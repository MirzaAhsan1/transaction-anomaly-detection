"""
Local regex-based field extraction from OCR text.

Extracts structured fields by applying bank-specific or generic regex patterns.
Each extracted field has an individual confidence score based on match quality.
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional

from ml.receipt_parser.bank_patterns import (
    detect_bank,
    get_field_patterns,
)


def _match_confidence(match: re.Match, field_name: str, text: str) -> float:
    """
    Calculate confidence score for a regex match.

    Factors:
    - Exact match (no extra surrounding text) → higher confidence
    - Match near expected keywords → higher confidence
    - Field type (amount, date are high confidence if found)
    """
    if not match:
        return 0.0

    matched_text = match.group(0)
    captured = match.group(1) if match.lastindex else match.group(0)

    base_confidence = 0.5

    # Amount matches near currency keywords are more reliable
    if field_name == "amount":
        base_confidence = 0.6
        if re.search(r"(?i)(total|amount|rs\.?|pkr|\$|due)", match.group(0)):
            base_confidence += 0.3

    # Date with proper format
    elif field_name == "date":
        base_confidence = 0.6
        try:
            parsed = _try_parse_date(captured)
            if parsed and parsed.year > 2000 and parsed.year < 2100:
                base_confidence += 0.3
        except Exception:
            pass

    # Transaction IDs that look alphanumeric are reliable
    elif field_name == "transaction_id":
        base_confidence = 0.5
        if re.match(r"^[A-Z0-9\-]{8,}$", captured, re.IGNORECASE):
            base_confidence += 0.3

    # Names - lower confidence as they can be misread by OCR
    elif field_name in ("sender_name", "receiver_name", "merchant_name"):
        base_confidence = 0.4
        # Longer names with spaces are more reliable
        if len(captured.split()) >= 2:
            base_confidence += 0.2
        if re.match(r"^[A-Za-z\s.]+$", captured.strip()):
            base_confidence += 0.2

    # Account numbers
    elif field_name in ("sender_account", "receiver_account"):
        base_confidence = 0.5
        digits = re.sub(r"[\s\-]", "", captured)
        if len(digits) >= 8:
            base_confidence += 0.3

    # Payment method / type
    elif field_name in ("payment_method", "transaction_type"):
        base_confidence = 0.4
        known_payment = ["credit card", "debit card", "bank transfer", "mobile wallet", "digital wallet"]
        known_types = ["transfer", "payment", "deposit", "withdrawal"]
        if captured.strip().lower() in known_payment + known_types:
            base_confidence += 0.4

    return min(base_confidence, 1.0)


def _try_parse_date(date_str: str) -> Optional[datetime]:
    """Try to parse a date string in common receipt formats."""
    date_str = date_str.strip()
    for fmt in [
        "%d-%m-%Y", "%d/%m/%Y", "%d %m %Y",
        "%m-%d-%Y", "%m/%d/%Y", "%m %d %Y",
        "%Y-%m-%d", "%Y/%m/%d",
        "%d-%b-%Y", "%d/%b/%Y", "%d %b %Y",
        "%b %d, %Y", "%d %B %Y",
    ]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def extract_fields(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract structured fields from OCR text using regex patterns.

    Args:
        text: Raw OCR text from receipt image

    Returns:
        Dict mapping field_name -> {"value": extracted_value, "confidence": float}
        Fields are mapped to our transaction schema names (not raw regex names).
    """
    if not text or not text.strip():
        return {}

    # 1. Detect bank
    bank_key, bank_config = detect_bank(text)
    field_patterns = get_field_patterns(bank_key)

    # 2. Extract raw fields using regex
    raw_extracted = {}
    for field_name, patterns in field_patterns.items():
        best_match = None
        best_confidence = 0.0

        for pattern in patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
            for match in matches:
                captured = match.group(1) if match.lastindex else match.group(0)
                confidence = _match_confidence(match, field_name, text)

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = captured.strip()

        if best_match:
            raw_extracted[field_name] = {
                "value": best_match,
                "confidence": round(best_confidence, 2),
            }

    # 3. Map raw field names to schema field names
    schema_mapping = {
        "amount": "amount",
        "date": "transaction_time",
        "transaction_id": None,  # not directly mapped to our schema
        "sender_name": "sender_name",
        "sender_account": "sender_account_number",
        "receiver_name": "receiver_name",
        "receiver_account": "receiver_account_number",
        "merchant_name": "merchant_name",
        "merchant_category": "merchant_category",
        "payment_method": "payment_method",
        "transaction_type": "transaction_type",
    }

    result = {}
    for raw_field, schema_field in schema_mapping.items():
        if schema_field is None:
            continue
        if raw_field in raw_extracted:
            result[schema_field] = raw_extracted[raw_field]

    return result


def get_extraction_summary(extracted: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Get summary statistics for extracted fields.

    Returns:
        Dict with: total_fields, extracted_count, average_confidence, bank_detected
    """
    required_fields = {"amount", "currency"}  # minimum required
    optional_fields = {
        "sender_name", "sender_account_number", "sender_bank",
        "receiver_name", "receiver_account_number", "receiver_bank",
        "merchant_name", "merchant_category",
        "payment_method", "transaction_type", "transaction_time",
    }

    extracted_required = required_fields.intersection(extracted.keys())
    extracted_optional = optional_fields.intersection(extracted.keys())

    confidences = [v["confidence"] for v in extracted.values() if isinstance(v, dict) and "confidence" in v]

    return {
        "total_extracted": len(extracted),
        "required_extracted": len(extracted_required),
        "optional_extracted": len(extracted_optional),
        "average_confidence": round(sum(confidences) / len(confidences), 2) if confidences else 0.0,
        "has_minimum_fields": len(extracted_required) == len(required_fields),
    }

