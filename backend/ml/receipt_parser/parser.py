"""
Receipt parser orchestrator.

Coordinates the full pipeline:
1. OCR: Extract raw text from image
2. Regex Extraction: Apply bank-specific/generic regex patterns
3. Gemini Extraction: Use AI for enhancement (if confidence is low or first pass)
4. Field Fusion: Merge results from both extractors, preferring higher confidence
5. Normalization: Clean and normalize all values
6. Response: Build structured ReceiptParseResult

This is the main entry point for the receipt parsing module.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from ml.receipt_parser.field_extractor import extract_fields, get_extraction_summary
from ml.receipt_parser.field_normalizer import (
    detect_currency,
    normalize_extracted_fields,
)
from ml.receipt_parser.ocr_engine import extract_text

# Gemini extraction is optional — only used if GEMINI_API_KEY is set
try:
    from ml.receipt_parser.gemini_extractor import (
        extract_fields_with_gemini,
        get_gemini_extraction_summary,
    )

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# Default confidence threshold below which Gemini enhancement is triggered
GEMINI_CONFIDENCE_THRESHOLD = 0.5


def _calculate_overall_confidence(
    extracted: Dict[str, Dict], gemini_extracted: Optional[Dict[str, Any]]
) -> float:
    """
    Calculate overall confidence based on how many required fields were extracted
    and the individual field confidences.
    """
    if not extracted and not gemini_extracted:
        return 0.0

    confidences = []
    for field_data in extracted.values():
        if isinstance(field_data, dict) and "confidence" in field_data:
            confidences.append(field_data["confidence"])

    regex_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    # If we have both, combine them (weighted average)
    if gemini_extracted and GEMINI_AVAILABLE:
        gemini_summary = get_gemini_extraction_summary(gemini_extracted, "")
        gemini_conf = gemini_summary.get("confidence", 0.0)

        # Gemini gets more weight if it extracted more fields
        gemini_fields = gemini_summary.get("fields_extracted", 0)
        gemini_weight = min(0.6, gemini_fields * 0.05)

        return round(
            regex_confidence * (1 - gemini_weight) + gemini_conf * gemini_weight, 2
        )

    return round(regex_confidence, 2)


def _merge_extractions(
    regex_extracted: Dict[str, Dict],
    gemini_extracted: Optional[Dict[str, Any]],
) -> Dict[str, Dict]:
    """
    Merge regex and Gemini extraction results.

    Strategy:
    - Prefer Gemini for fields where regex confidence is < 0.5
    - Prefer regex for fields where regex confidence is >= 0.7
    - For 0.5-0.7, use which one has a non-null value
    - Gemini fills in gaps that regex couldn't find
    """
    merged = dict(regex_extracted)  # start with regex results

    if not gemini_extracted or not GEMINI_AVAILABLE:
        return merged

    # Schema field mapping for Gemini output
    gemini_mapping = {k: k for k in merged.keys()}
    gemini_mapping.update(
        {
            "amount": "amount",
            "currency": "currency",
            "transaction_time": "transaction_time",
            "sender_name": "sender_name",
            "sender_account_number": "sender_account_number",
            "sender_bank": "sender_bank",
            "receiver_name": "receiver_name",
            "receiver_account_number": "receiver_account_number",
            "receiver_bank": "receiver_bank",
            "merchant_name": "merchant_name",
            "merchant_category": "merchant_category",
            "payment_method": "payment_method",
            "transaction_type": "transaction_type",
        }
    )

    for gemini_field, schema_field in gemini_mapping.items():
        gemini_value = gemini_extracted.get(gemini_field)
        if gemini_value is None:
            continue

        if schema_field not in merged:
            # Gemini found a field regex missed
            merged[schema_field] = {
                "value": gemini_value,
                "confidence": 0.6,  # moderate confidence for Gemini-only fields
            }
        else:
            # Both have value — update confidence if Gemini is better
            current = merged[schema_field]
            if current.get("confidence", 0) < 0.5:
                merged[schema_field] = {
                    "value": gemini_value,
                    "confidence": round(
                        max(current.get("confidence", 0), 0.6), 2
                    ),
                }

    return merged


def parse_receipt_image(image_bytes: bytes, use_gemini: bool = True) -> Dict[str, Any]:
    """
    Main entry point for receipt parsing.

    Pipeline:
    1. OCR text extraction
    2. Regex-based field extraction with bank detection
    3. Optional Gemini AI enhancement
    4. Field fusion and normalization
    5. Build result with confidence scores

    Args:
        image_bytes: Raw image file bytes (JPEG, PNG, etc.)
        use_gemini: Whether to attempt Gemini AI enhancement

    Returns:
        Dict with:
        - All extracted fields matching ReceiptParseResult schema
        - confidence: Overall confidence score
        - raw_text_preview: First 5000 chars of OCR text
        - extraction_method: How fields were extracted
        - notes: Any warnings or context
    """
    # Step 1: OCR
    ocr_text = extract_text(image_bytes)

    # Step 2: Regex extraction with bank detection
    regex_extracted = extract_fields(ocr_text)
    regex_summary = get_extraction_summary(regex_extracted)
    bank_detected = None

    # Detect bank for context
    from ml.receipt_parser.bank_patterns import detect_bank

    detected_bank_key, detected_bank_config = detect_bank(ocr_text)
    bank_detected = detected_bank_config["name"] if detected_bank_config else None

    # Step 3: Gemini enhancement (optional)
    gemini_extracted = None
    gemini_used = False
    if (
        use_gemini
        and GEMINI_AVAILABLE
        and regex_summary.get("average_confidence", 0) < GEMINI_CONFIDENCE_THRESHOLD
    ):
        try:
            gemini_extracted = extract_fields_with_gemini(
                ocr_text, bank_context=bank_detected
            )
            gemini_used = True
        except (RuntimeError, ValueError):
            # Gemini failed — continue with regex results only
            pass

    # Step 4: Merge regex + Gemini
    merged = _merge_extractions(regex_extracted, gemini_extracted)

    # Step 5: Normalize values
    normalized = normalize_extracted_fields(merged)

    # Step 6: Calculate confidence
    overall_confidence = _calculate_overall_confidence(
        normalized, gemini_extracted
    )

    # Step 7: Detect currency from text if not extracted
    currency = None
    if "currency" in normalized:
        currency = normalized["currency"]["value"]
    else:
        currency = detect_currency(ocr_text)

    # Step 8: Build result
    amount = normalized.get("amount", {}).get("value") if normalized.get("amount") else None
    transaction_time = normalized.get("transaction_time", {}).get("value") if normalized.get("transaction_time") else None

    # Prepare the final flat result dict
    result = {
        "amount": amount,
        "currency": currency,
        "transaction_time": transaction_time,
        "sender_name": normalized.get("sender_name", {}).get("value") if normalized.get("sender_name") else None,
        "sender_account_number": normalized.get("sender_account_number", {}).get("value") if normalized.get("sender_account_number") else None,
        "sender_bank": normalized.get("sender_bank", {}).get("value") if normalized.get("sender_bank") else None,
        "receiver_name": normalized.get("receiver_name", {}).get("value") if normalized.get("receiver_name") else None,
        "receiver_account_number": normalized.get("receiver_account_number", {}).get("value") if normalized.get("receiver_account_number") else None,
        "receiver_bank": normalized.get("receiver_bank", {}).get("value") if normalized.get("receiver_bank") else None,
        "merchant_name": normalized.get("merchant_name", {}).get("value") if normalized.get("merchant_name") else None,
        "merchant_category": normalized.get("merchant_category", {}).get("value") if normalized.get("merchant_category") else None,
        "payment_method": normalized.get("payment_method", {}).get("value") if normalized.get("payment_method") else None,
        "transaction_type": normalized.get("transaction_type", {}).get("value") if normalized.get("transaction_type") else None,
        "confidence": overall_confidence,
        "extraction_method": "regex+gemini" if gemini_used else "regex",
        "bank_detected": bank_detected,
        "raw_text_preview": ocr_text[:5000],
        "notes": (
            "Automatically extracted from receipt. Please review fields before submitting."
            if overall_confidence < 0.8
            else "High confidence extraction. Fields should be accurate."
        ),
    }

    return result

