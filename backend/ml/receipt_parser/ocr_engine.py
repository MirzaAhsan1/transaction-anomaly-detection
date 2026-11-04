"""
OCR Engine abstraction.

Provides fallback chain: easyocr → pytesseract → paddleocr
If none available, raises clear error with installation instructions.
"""

import io
from typing import Optional

import numpy as np
from PIL import Image


def _load_image(image_bytes: bytes) -> np.ndarray:
    """Convert image bytes to numpy array for OCR libraries."""
    img = Image.open(io.BytesIO(image_bytes))
    img_rgb = img.convert("RGB")
    return np.array(img_rgb)


def _ocr_easyocr(image_np: np.ndarray) -> Optional[str]:
    """OCR using easyocr library."""
    try:
        import easyocr

        reader = easyocr.Reader(["en"], gpu=False)
        result = reader.readtext(image_np)
        lines = [r[1] for r in result if len(r) >= 2]
        text = "\n".join(lines).strip()
        return text if text else None
    except ImportError:
        return None
    except Exception as e:
        raise RuntimeError(f"easyocr failed: {e}") from e


def _ocr_pytesseract(image_np: np.ndarray) -> Optional[str]:
    """OCR using pytesseract (Tesseract) library."""
    try:
        import pytesseract

        from PIL import Image

        pil_img = Image.fromarray(image_np)
        text = pytesseract.image_to_string(pil_img)
        text = text.strip()
        return text if text else None
    except ImportError:
        return None
    except Exception as e:
        raise RuntimeError(f"pytesseract failed: {e}") from e


def _ocr_paddleocr(image_np: np.ndarray) -> Optional[str]:
    """OCR using PaddleOCR library."""
    try:
        from paddleocr import PaddleOCR

        ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
        result = ocr.ocr(image_np, cls=True)
        lines = []
        if result and result[0]:
            for line in result[0]:
                if len(line) >= 2:
                    lines.append(line[1][0])
        text = "\n".join(lines).strip()
        return text if text else None
    except ImportError:
        return None
    except Exception as e:
        raise RuntimeError(f"paddleocr failed: {e}") from e


def extract_text(image_bytes: bytes) -> str:
    """
    Extract text from receipt image using best available OCR engine.

    Fallback chain:
    1. easyocr (deep learning, best accuracy)
    2. pytesseract (Tesseract, good for clean text)
    3. paddleocr (another deep learning option)

    Raises:
        RuntimeError: If no OCR library available or all engines fail.
    """
    if not image_bytes:
        raise ValueError("Empty image bytes")

    image_np = _load_image(image_bytes)

    # Try easyocr first (best accuracy)
    text = _ocr_easyocr(image_np)
    if text:
        return text

    # Fallback to pytesseract
    text = _ocr_pytesseract(image_np)
    if text:
        return text

    # Fallback to paddleocr
    text = _ocr_paddleocr(image_np)
    if text:
        return text

    raise RuntimeError(
        "No OCR library available or all OCR engines failed.\n"
        "Install at least one:\n"
        "  pip install easyocr        (recommended)\n"
        "  pip install pytesseract    (requires tesseract-ocr system package)\n"
        "  pip install paddleocr      (alternative DL OCR)"
    )

