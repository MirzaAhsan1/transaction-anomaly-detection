"""
Gemini AI-based field extraction from OCR text.

Uses Google's Gemini API to extract structured fields from receipt text.
Works on ANY receipt format regardless of layout, making it ideal for
unknown bank formats or receipts with unusual layouts.

Requires GEMINI_API_KEY environment variable to be set.
"""

import json
import os
import re
from typing import Any, Dict, Optional


def _get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from environment variable."""
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def extract_fields_with_gemini(
    ocr_text: str,
    content_hint: str = "",
    bank_context: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract structured fields from OCR text using Gemini AI.

    Args:
        ocr_text: Raw text from OCR
        content_hint: Optional context hint (e.g., "This is a Meezan Bank receipt")
        bank_context: Optional detected bank name for better extraction

    Returns:
        Dict with fields matching the transaction schema:
        amount, currency, transaction_time, sender_name, sender_account_number,
        sender_bank, receiver_name, receiver_account_number, receiver_bank,
        merchant_name, merchant_category, payment_method, transaction_type

    Raises:
        RuntimeError: If Gemini API key is missing or API call fails.
        ValueError: If response cannot be parsed as JSON.
    """
    api_key = _get_gemini_api_key()
    if not api_key:
        raise RuntimeError(
            "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
        )

    # Try google-generativeai SDK
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        bank_context_str = (
            f"The receipt appears to be from {bank_context}." if bank_context else ""
        )

        prompt = f"""
You are an expert at parsing payment receipts from ANY bank or payment provider.
The receipt layout can vary widely between different banks and formats.

{bank_context_str}

Task:
From the following OCR text, extract the transaction/payment fields and return STRICT JSON only.

Rules:
- Return JSON with these exact keys (use null when unknown):
  amount, currency, transaction_time, sender_name, sender_account_number, sender_bank,
  receiver_name, receiver_account_number, receiver_bank,
  merchant_name, merchant_category,
  payment_method, transaction_type
- amount must be a number (float), NOT a string. If a currency symbol is present, set currency accordingly.
- transaction_time should be ISO 8601 string if possible; otherwise return the raw date string as-is.
- payment_method options: Credit Card, Debit Card, Bank Transfer, Mobile Wallet, Digital Wallet, Cash
- transaction_type options: Transfer, Payment, Withdrawal, Deposit, Purchase
- For Pakistani bank receipts: amounts are likely in PKR.
- If you see account numbers starting with X or * (masked), extract them as-is.
- Extract bank names from the receipt text (sender_bank, receiver_bank).
- If a field is not found in the receipt, set it to null (do NOT make up values).

OCR text:
```
{ocr_text}
```

{content_hint}

Return ONLY valid JSON, no other text.
""".strip()

        resp = model.generate_content(prompt)
        raw = getattr(resp, "text", None) or str(resp)

        # Extract first JSON object in case model wraps it in markdown
        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            raise ValueError(f"Gemini did not return JSON. Raw response: {raw[:500]}")

        data = json.loads(match.group(0))
        return data

    except ImportError as e:
        raise RuntimeError(
            "Gemini SDK not installed. Install with: pip install google-generativeai"
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini response as JSON: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}") from e


def get_gemini_extraction_summary(
    extracted: Dict[str, Any], ocr_text: str
) -> Dict[str, Any]:
    """
    Get confidence summary for Gemini-based extraction.

    Returns dict with:
    - fields_extracted: number of non-null fields
    - has_required: whether amount and currency are present
    - confidence: estimated confidence based on completeness
    """
    non_null_fields = {k: v for k, v in extracted.items() if v is not None}
    required_present = all(
        extracted.get(f) is not None for f in ("amount", "currency")
    )

    # Estimate confidence based on:
    # - How many fields extracted (out of 14)
    # - Whether required fields (amount, currency) are present
    field_ratio = len(non_null_fields) / 14.0
    confidence = field_ratio * 0.7 + (0.3 if required_present else 0)

    return {
        "fields_extracted": len(non_null_fields),
        "has_required": required_present,
        "confidence": round(min(confidence, 1.0), 2),
        "extracted_fields": list(non_null_fields.keys()),
    }

