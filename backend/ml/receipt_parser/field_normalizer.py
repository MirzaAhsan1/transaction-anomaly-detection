"""
Field normalization utilities for receipt parsing.

Handles:
- Amount normalization (Rs. 1,000.50 → 1000.50)
- Date parsing (multiple formats → ISO 8601)
- Bank name standardization
- Currency detection
- Account number cleanup
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional


def normalize_amount(raw_value: Any) -> Optional[float]:
    """
    Normalize amount value from receipt text.

    Handles:
    - "Rs. 1,000.50" → 1000.50
    - "PKR 1,000" → 1000.0
    - "$1,234.56" → 1234.56
    - "1.000,50" (European format) → 1000.50
    - "1,234" → 1234.0
    """
    if raw_value is None:
        return None

    s = str(raw_value).strip()
    if not s:
        return None

    # Remove currency symbols and text
    s = re.sub(r"(?i)(rs\.?\s*|pkr\s*|\$\s*|€\s*|£\s*|usd\s*|eur\s*|gbp\s*)", "", s)
    s = s.strip()

    # Handle European format: 1.000,50 (dot as thousand sep, comma as decimal)
    if re.match(r"^\d{1,3}(\.\d{3})+(,\d{1,2})?$", s):
        s = s.replace(".", "")
        s = s.replace(",", ".")
    # Handle standard format with commas: 1,234.56
    elif "," in s and "." in s:
        # Check if comma is thousand separator (standard)
        if s.rindex(",") < s.rindex("."):
            s = s.replace(",", "")
        # Otherwise comma is decimal separator (European)
        else:
            s = s.replace(".", "")
            s = s.replace(",", ".")
    # Only commas: could be decimal or thousand separator
    elif "," in s and "." not in s:
        # If only one comma at position -3 or -2, it's likely decimal
        if re.search(r",\d{2}$", s):
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")

    try:
        return round(float(s), 2)
    except (ValueError, TypeError):
        return None


def normalize_date(raw_value: Any) -> Optional[str]:
    """
    Normalize date value from receipt text to ISO 8601 string.

    Handles formats:
    - DD-MM-YYYY, DD/MM/YYYY
    - MM-DD-YYYY, MM/DD/YYYY
    - YYYY-MM-DD
    - DD-Mon-YYYY, DD/Mon/YYYY
    - Mon DD, YYYY
    - DD Month YYYY
    """
    if raw_value is None:
        return None

    s = str(raw_value).strip()
    if not s:
        return None

    # Remove time component if present, we only want date
    s = re.sub(r"\s+\d{2}:\d{2}(:\d{2})?.*$", "", s).strip()

    # Try to detect and parse date
    # Priority: DD-MM-YYYY > MM-DD-YYYY > YYYY-MM-DD
    date_formats = [
        # Day first formats (common in Pakistan/UK)
        ("%d-%m-%Y", r"^\d{2}-\d{2}-\d{4}$"),
        ("%d/%m/%Y", r"^\d{2}/\d{2}/\d{4}$"),
        ("%d %m %Y", r"^\d{2}\s+\d{2}\s+\d{4}$"),
        ("%d-%b-%Y", r"^\d{2}-[A-Za-z]{3}-\d{4}$"),
        ("%d/%b/%Y", r"^\d{2}/[A-Za-z]{3}/\d{4}$"),
        ("%d %b %Y", r"^\d{2}\s+[A-Za-z]{3}\s+\d{4}$"),
        # Month first formats (US common)
        ("%m-%d-%Y", r"^\d{2}-\d{2}-\d{4}$"),
        ("%m/%d/%Y", r"^\d{2}/\d{2}/\d{4}$"),
        ("%b %d, %Y", r"^[A-Za-z]{3}\s+\d{1,2},?\s+\d{4}$"),
        ("%B %d, %Y", r"^[A-Za-z]+\s+\d{1,2},?\s+\d{4}$"),
        # Year first formats
        ("%Y-%m-%d", r"^\d{4}-\d{2}-\d{2}$"),
        ("%Y/%m/%d", r"^\d{4}/\d{2}/\d{2}$"),
        # Long month names
        ("%d %B %Y", r"^\d{2}\s+[A-Za-z]+\s+\d{4}$"),
    ]

    for fmt, pattern in date_formats:
        try:
            parsed = datetime.strptime(s, fmt)
            return parsed.isoformat()
        except ValueError:
            continue

    return None


def normalize_bank_name(raw_value: Any) -> Optional[str]:
    """
    Normalize bank name to standard format.

    Maps variations like:
    - "Meezan Bank Ltd." → "Meezan Bank"
    - "HBL" → "Habib Bank Limited"
    - "Allied Bank Limited" → "Allied Bank"
    """
    if raw_value is None:
        return None

    s = str(raw_value).strip()

    bank_mapping = {
        r"(?i)mee.?zan": "Meezan Bank",
        r"(?i)\bHBL\b": "Habib Bank Limited (HBL)",
        r"(?i)habib": "Habib Bank Limited (HBL)",
        r"(?i)allied": "Allied Bank",
        r"(?i)united\s*bank": "United Bank Limited (UBL)",
        r"(?i)\bUBL\b": "United Bank Limited (UBL)",
        r"(?i)al\s*falah": "Bank Al Falah",
        r"(?i)alfalah": "Bank Al Falah",
        r"(?i)mc.bank": "MCB Bank",
        r"(?i)muslim\s*commercial": "MCB Bank",
        r"(?i)standard\s*chartered": "Standard Chartered",
        r"(?i)saday.?pay": "SadayPay",
        r"(?i)easy.?paisa": "Easypaisa",
        r"(?i)naya.?pay": "NayaPay",
        r"(?i)keenu": "Keenu Wallet",
        r"(?i)jazz.?cash": "JazzCash",
        r"(?i)\bchase\b": "Chase Bank",
        r"(?i)bank\s*of\s*america": "Bank of America",
        r"(?i)wells\s*fargo": "Wells Fargo",
        r"(?i)citibank": "Citibank",
    }

    for pattern, standard_name in bank_mapping.items():
        if re.search(pattern, s):
            return standard_name

    return s  # return original if no mapping found


def detect_currency(text: str) -> str:
    """
    Detect currency from receipt text.

    Returns ISO 4217 currency code (USD, PKR, EUR, GBP, etc.)
    Defaults to "PKR" for Pakistani receipts.
    """
    if not text:
        return "PKR"

    currency_patterns = [
        (r"(?i)pkr|rs\.?\s*|rupees?\s*", "PKR"),
        (r"\$|\bUSD\b|\bdollar", "USD"),
        (r"€|\bEUR\b|\beuro", "EUR"),
        (r"£|\bGBP\b|\ppound", "GBP"),
        (r"CAD|\bcanadian\s*dollar", "CAD"),
        (r"AUD|\baustralian\s*dollar", "AUD"),
    ]

    for pattern, currency_code in currency_patterns:
        if re.search(pattern, text):
            return currency_code

    # Check bank context - Pakistani banks default to PKR
    bank_detection_patterns = [
        r"(?i)mee.?zan",
        r"(?i)habib",
        r"(?i)\bHBL\b",
        r"(?i)allied",
        r"(?i)united\s*bank",
        r"(?i)saday.?pay",
        r"(?i)easy.?paisa",
        r"(?i)naya.?pay",
    ]

    for pattern in bank_detection_patterns:
        if re.search(pattern, text):
            return "PKR"

    return "PKR"  # default


def normalize_account_number(raw_value: Any) -> Optional[str]:
    """
    Normalize account number by removing spaces, dashes, and masking characters.
    """
    if raw_value is None:
        return None

    s = str(raw_value).strip()
    # Remove X's and *'s (masked characters)
    s = re.sub(r"[Xx\*]", "", s)
    # Remove spaces and dashes
    s = re.sub(r"[\s\-]", "", s)

    return s if s else None


def normalize_extracted_fields(extracted: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Apply all normalizers to extracted fields.

    Args:
        extracted: Dict mapping schema_field -> {"value": raw, "confidence": float}

    Returns:
        Dict with normalized values
    """
    normalized = {}

    for field_name, field_data in extracted.items():
        if not isinstance(field_data, dict):
            continue

        raw_value = field_data.get("value")
        confidence = field_data.get("confidence", 0.0)

        if field_name == "amount":
            norm_value = normalize_amount(raw_value)
            if norm_value is not None:
                normalized[field_name] = {
                    "value": norm_value,
                    "confidence": confidence + 0.1,  # boost confidence for successful normalization
                }

        elif field_name == "transaction_time":
            norm_value = normalize_date(raw_value)
            if norm_value is not None:
                normalized[field_name] = {
                    "value": norm_value,
                    "confidence": confidence + 0.1,
                }

        elif field_name == "sender_bank" or field_name == "receiver_bank":
            norm_value = normalize_bank_name(raw_value)
            if norm_value is not None:
                normalized[field_name] = {
                    "value": norm_value,
                    "confidence": confidence,
                }

        elif field_name in ("sender_account_number", "receiver_account_number"):
            norm_value = normalize_account_number(raw_value)
            if norm_value is not None:
                normalized[field_name] = {
                    "value": norm_value,
                    "confidence": confidence,
                }

        elif field_name in ("merchant_name", "sender_name", "receiver_name"):
            # Clean names - remove trailing punctuation, whitespace
            clean = str(raw_value).strip().rstrip(".,;:")
            normalized[field_name] = {
                "value": clean,
                "confidence": confidence,
            }

        else:
            # Pass through as-is
            normalized[field_name] = {
                "value": raw_value,
                "confidence": confidence,
            }

    return normalized

