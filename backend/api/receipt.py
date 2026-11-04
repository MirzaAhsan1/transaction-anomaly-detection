from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile

from core.config import settings
from schemas.receipt import ReceiptParseResult

# Import the new receipt parser module
from ml.receipt_parser import parse_receipt_image
from ml.receipt_parser.ocr_engine import extract_text as ocr_image_to_text

router = APIRouter(prefix="/api/receipt", tags=["receipt"])


def _try_parse_datetime(s: Any) -> Optional[datetime]:
    """Parse a datetime from various string formats."""
    if s is None:
        return None
    if isinstance(s, datetime):
        return s
    s = str(s).strip()
    if not s:
        return None

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass

    return None


@router.post("/parse", response_model=ReceiptParseResult)
def parse_receipt(image: UploadFile = File(...)) -> ReceiptParseResult:
    """
    Parse a payment receipt image and extract structured transaction data.

    The pipeline:
    1. OCR extraction (easyocr -> pytesseract -> paddleocr fallback)
    2. Bank detection and regex-based field extraction
       (Meezan, HBL, Allied, UBL, SadayPay, Easypaisa, etc.)
    3. Optional Gemini AI enhancement (if GEMINI_API_KEY is set)
    4. Field fusion and normalization
    5. Return structured result for frontend auto-fill

    Works with ANY receipt format - bank-specific regex + AI fallback.
    """
    # Validate upload
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")

    image_bytes = image.file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty upload")

    # Determine if Gemini API is available
    use_gemini = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

    try:
        # Use the new parser module
        result = parse_receipt_image(image_bytes, use_gemini=use_gemini)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Receipt parsing failed: {e}",
        ) from e

    # Build response
    transaction_time = _try_parse_datetime(result.get("transaction_time"))

    parse_res = ReceiptParseResult(
        amount=result.get("amount"),
        currency=result.get("currency"),
        transaction_time=transaction_time,
        sender_name=result.get("sender_name"),
        sender_account_number=result.get("sender_account_number"),
        sender_bank=result.get("sender_bank"),
        receiver_name=result.get("receiver_name"),
        receiver_account_number=result.get("receiver_account_number"),
        receiver_bank=result.get("receiver_bank"),
        merchant_name=result.get("merchant_name"),
        merchant_category=result.get("merchant_category"),
        payment_method=result.get("payment_method"),
        transaction_type=result.get("transaction_type"),
        confidence=result.get("confidence", 0.0),
        extraction_method=result.get("extraction_method", "regex"),
        bank_detected=result.get("bank_detected"),
        raw_text_preview=result.get("raw_text_preview"),
        notes=result.get("notes"),
    )

    return parse_res

