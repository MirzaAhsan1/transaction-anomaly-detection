"""
Bank-specific regex patterns for Pakistani and international banks.

Each bank entry contains:
- name: Display name
- detection_patterns: List of regex patterns to identify this bank from receipt text
- field_patterns: Dict of field_name -> list of regex patterns to extract that field
- account_format: Description of account number format for validation

Adding a new bank:
1. Add a new entry to BANK_PATTERNS dict
2. Add detection_patterns (text that appears on this bank's receipts)
3. Add field_patterns for: amount, date, transaction_id, sender, receiver, etc.
4. The system will auto-detect and apply your patterns
"""

import re

# ─── Bank Pattern Definitions ───────────────────────────────────────────────

BANK_PATTERNS = {
    "meezen": {
        "name": "Meezan Bank",
        "detection_patterns": [
            r"(?i)mee.?zan\s*bank",
            r"(?i)meezan\s*islamic",
            r"(?i)al\s*mee.?zan",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)amount\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)total\s*(?:amount)?\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
                r"(?i)pkr\s*([\d,]+\.?\d*)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
                r"(\d{2}[-\s/][A-Za-z]{3}[-\s/]\d{4})",
                r"date\s*:?\s*(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:tr(?:ans)?(?:action)?\s*(?:id|#|no|number)?\s*:?\s*)([A-Z0-9\-]+)",
                r"(?i)(?:ref(?:erence)?\s*(?:id|#|no|number)?\s*:?\s*)([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|sender|sent\s*by|debited\s*from)\s*:?\s*([A-Za-z\s.]+?)(?:\n|\||\d)",
                r"(?i)(?:from|sender)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "sender_account": [
                r"(?i)(?:from|sender|debit)\s*(?:account|a/c|acc)?\s*:?\s*([\d\-Xx*]{4,})",
                r"(?i)(?:account|a/c|acc)\s*(?:#|no|number)?\s*:?\s*([\d\-]{4,})",
            ],
            "receiver_name": [
                r"(?i)(?:to|receiver|beneficiary|pay\s*to|credited\s*to)\s*:?\s*([A-Za-z\s.]+?)(?:\n|\||\d)",
                r"(?i)(?:to|receiver)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "receiver_account": [
                r"(?i)(?:to|receiver|credit)\s*(?:account|a/c|acc)?\s*:?\s*([\d\-Xx*]{4,})",
                r"(?i)(?:iban|account)\s*(?:#|no|number)?\s*:?\s*([A-Z]{2}\d{2}[\dA-Z]{10,})",
            ],
        },
    },
    "hbl": {
        "name": "Habib Bank Limited (HBL)",
        "detection_patterns": [
            r"(?i)habib\s*bank",
            r"(?i)\bHBL\b",
            r"(?i)habib\s*metropolitan",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total|rs)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
                r"(?i)pkr\s*([\d,]+\.?\d*)",
                r"([\d,]+\.\d{2})\s*(?:pkr|rs\.?)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
                r"(\d{4}[-\s/]\d{2}[-\s/]\d{2})",
                r"date\s*:?\s*(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|transaction)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
                r"(?i)ref\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|sender|debited)\s*:?\s*([A-Za-z\s.]+?)(?:\n|\||\d)",
            ],
            "sender_account": [
                r"(?i)(?:from|debit)\s*(?:account|a/c)?\s*:?\s*([\d\-Xx*]{4,})",
            ],
            "receiver_name": [
                r"(?i)(?:to|receiver|beneficiary|credited)\s*:?\s*([A-Za-z\s.]+?)(?:\n|\||\d)",
            ],
            "receiver_account": [
                r"(?i)(?:to|credit)\s*(?:account|a/c)?\s*:?\s*([\d\-Xx*]{4,})",
            ],
        },
    },
    "allied": {
        "name": "Allied Bank Limited",
        "detection_patterns": [
            r"(?i)allied\s*bank",
            r"(?i)abl",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total|rs)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
                r"date\s*:?\s*(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|receipt)\s*(?:#|no|id)?\s*:?\s*([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|sender)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "sender_account": [
                r"(?i)(?:from|sender|debit)\s*(?:account|a/c)?\s*:?\s*([\d\-Xx*]{4,})",
            ],
            "receiver_name": [
                r"(?i)(?:to|receiver|payee)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "receiver_account": [
                r"(?i)(?:to|credit|receiver)\s*(?:account|a/c)?\s*:?\s*([\d\-Xx*]{4,})",
            ],
        },
    },
    "ubl": {
        "name": "United Bank Limited (UBL)",
        "detection_patterns": [
            r"(?i)united\s*bank",
            r"(?i)\bUBL\b",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
                r"(?i)pkr\s*([\d,]+\.?\d*)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
                r"date\s*:?\s*(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|transaction)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|sender|debited)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "sender_account": [
                r"(?i)(?:from|debit)\s*(?:account|a/c)?\s*:?\s*([\d\-Xx*]{4,})",
            ],
            "receiver_name": [
                r"(?i)(?:to|receiver|beneficiary)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "receiver_account": [
                r"(?i)(?:to|credit)\s*(?:account|a/c)?\s*:?\s*([\d\-Xx*]{4,})",
            ],
        },
    },
    "sadaypay": {
        "name": "SadayPay",
        "detection_patterns": [
            r"(?i)saday.?pay",
            r"(?i)sadaypay",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total|rs)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
                r"([\d,]+\.\d{2})\s*(?:pkr|rs\.?)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
                r"date\s*:?\s*(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|receipt|payment)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|sender|payer)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "receiver_name": [
                r"(?i)(?:to|receiver|payee|merchant)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "sender_account": [
                r"(?i)(?:from|wallet|mobile)\s*(?:#|no)?\s*:?\s*([\d\-+]{4,})",
            ],
            "receiver_account": [
                r"(?i)(?:to|wallet|account)\s*(?:#|no)?\s*:?\s*([\d\-+]{4,})",
            ],
            "merchant_name": [
                r"(?i)(?:merchant|store|shop)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
        },
    },
    "easypaisa": {
        "name": "Easypaisa",
        "detection_patterns": [
            r"(?i)easy.?paisa",
            r"(?i)easypaisa",
            r"(?i)easy\s*paisa",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total|rs)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
                r"([\d,]+\.\d{2})\s*(?:pkr|rs\.?)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
                r"date\s*:?\s*(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|receipt|payment)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|sender|payer)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "receiver_name": [
                r"(?i)(?:to|receiver|payee|merchant)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "sender_account": [
                r"(?i)(?:from|wallet|mobile|account)\s*(?:#|no)?\s*:?\s*([\d\-+]{7,})",
            ],
            "receiver_account": [
                r"(?i)(?:to|wallet|account)\s*(?:#|no)?\s*:?\s*([\d\-+]{7,})",
            ],
        },
    },
    "naya_pay": {
        "name": "NayaPay",
        "detection_patterns": [
            r"(?i)naya.?pay",
            r"(?i)nayapay",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
                r"(?i)rs\.?\s*([\d,]+\.?\d*)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|payment)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
            "sender_name": [
                r"(?i)(?:from|payer)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
            "receiver_name": [
                r"(?i)(?:to|payee)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
            ],
        },
    },
    "sadaf_pay": {
        "name": "SadafPay",
        "detection_patterns": [
            r"(?i)sadaf.?pay",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
        },
    },
    "keenu_wallet": {
        "name": "Keenu Wallet",
        "detection_patterns": [
            r"(?i)keenu.?wallet",
            r"(?i)keenuwallet",
        ],
        "field_patterns": {
            "amount": [
                r"(?i)(?:amount|total)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
            ],
            "date": [
                r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
            ],
            "transaction_id": [
                r"(?i)(?:trx|txn|payment)\s*(?:id|#|no)?\s*:?\s*([A-Z0-9\-]+)",
            ],
        },
    },
}

# ─── Generic Patterns (fallback when no bank detected) ─────────────────────

GENERIC_FIELD_PATTERNS = {
    "amount": [
        r"(?i)(?:amount|total|sum|payment)\s*:?\s*(?:rs\.?|pkr|\$|€|£)?\s*([\d,]+\.?\d*)",
        r"(?i)(?:rs\.?|pkr|\$|€|£)\s*([\d,]+\.?\d*)",
        r"(?i)(?:total\s*(?:amount)?|amount\s*due)\s*:?\s*(?:rs\.?|pkr)?\s*([\d,]+\.?\d*)",
        r"([\d,]+\.\d{2})\s*(?:pkr|rs\.?|\$|€|£)",
    ],
    "date": [
        r"(\d{2}[-\s/]\d{2}[-\s/]\d{4})",
        r"(\d{4}[-\s/]\d{2}[-\s/]\d{2})",
        r"(\d{2}[-\s/][A-Za-z]{3}[-\s/]\d{4})",
        r"([A-Za-z]+\s+\d{1,2},?\s*\d{4})",
        r"(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
    ],
    "transaction_id": [
        r"(?i)(?:tr(?:ans)?(?:action)?\s*(?:id|#|no|number)?\s*:?\s*)([A-Z0-9\-]{6,})",
        r"(?i)(?:ref(?:erence)?\s*(?:id|#|no|number)?\s*:?\s*)([A-Z0-9\-]{6,})",
        r"(?i)(?:receipt|payment|invoice)\s*(?:#|no|id|number)?\s*:?\s*([A-Z0-9\-]{6,})",
    ],
    "sender_name": [
        r"(?i)(?:from|sender|sent\s*by|payer|debited\s*from)\s*:?\s*([A-Za-z\s.]+?)(?:\n|\||\d)",
        r"(?i)(?:from|sender|payer)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
    ],
    "sender_account": [
        r"(?i)(?:from|sender|debit|payer)\s*(?:account|a/c|acc|wallet)?\s*:?\s*([\d\-Xx*]{4,})",
        r"(?i)(?:account|a/c|acc)\s*(?:#|no|number)?\s*:?\s*([\d\-]{4,})",
    ],
    "receiver_name": [
        r"(?i)(?:to|receiver|beneficiary|pay\s*to|credited\s*to|payee)\s*:?\s*([A-Za-z\s.]+?)(?:\n|\||\d)",
        r"(?i)(?:to|receiver|beneficiary|payee)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
    ],
    "receiver_account": [
        r"(?i)(?:to|receiver|credit|payee)\s*(?:account|a/c|acc|wallet)?\s*:?\s*([\d\-Xx*]{4,})",
        r"(?i)(?:iban)\s*(?:#|no|number)?\s*:?\s*([A-Z]{2}\d{2}[\dA-Z]{10,})",
    ],
    "merchant_name": [
        r"(?i)(?:merchant|store|shop|vendor|business)\s*:?\s*([A-Za-z\s.]+?)(?:\n|$)",
    ],
    "payment_method": [
        r"(?i)(?:payment method|method|via)\s*:?\s*([A-Za-z\s]+?)(?:\n|$)",
        r"(?i)(?:credit card|debit card|bank transfer|mobile wallet|digital wallet)",
    ],
    "transaction_type": [
        r"(?i)(?:transaction type|type)\s*:?\s*([A-Za-z\s]+?)(?:\n|$)",
        r"(?i)\b(transfer|payment|deposit|withdrawal)\b",
    ],
}


def detect_bank(text: str) -> tuple:
    """
    Detect which bank issued the receipt based on OCR text.

    Returns:
        Tuple of (bank_key: str, bank_config: dict or None)
        bank_key is the key in BANK_PATTERNS, or 'generic' if unknown.
    """
    text_lower = text.lower()

    for bank_key, bank_config in BANK_PATTERNS.items():
        for pattern in bank_config["detection_patterns"]:
            if re.search(pattern, text):
                return bank_key, bank_config

    return "generic", None


def get_field_patterns(bank_key: str) -> dict:
    """
    Get regex patterns for field extraction, either bank-specific or generic.
    """
    if bank_key in BANK_PATTERNS:
        return BANK_PATTERNS[bank_key]["field_patterns"]
    return GENERIC_FIELD_PATTERNS

