# Receipt Parser Enhancement Plan

## Objective
Build a robust receipt parsing API that works on **any receipt format** (Meezan Bank, SadayPay, Allied Bank, HBL, UBL, etc.) and auto-fills the transaction form.

---

## How It Will Work (Pipeline)

```
User uploads receipt image (any format)
                │
                ▼
┌──────────────────────────────────────┐
│  Step 1: OCR Engine                  │
│  (extract text from image)           │
│                                      │
│  Tools (tried in order):             │
│  1. easyocr (deep learning OCR)      │
│  2. pytesseract (Tesseract OCR)      │
│  3. paddleocr (alternative DL OCR)   │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│  Step 2: Field Extraction Layer      │
│  (extract structured fields from     │
│   raw text)                          │
│                                      │
│  Two parallel approaches:            │
│                                      │
│  A. Local Regex Extractor            │
│     - Bank-specific patterns         │
│       (Meezan, Allied, HBL, UBL,     │
│        SadayPay, Easypaisa, etc.)    │
│     - Generic patterns (amount,      │
│       date, account numbers)         │
│     - Returns extracted fields       │
│       + confidence score             │
│                                      │
│  B. Gemini AI Extractor (enhancement)│
│     - Sends raw OCR text to Gemini   │
│     - Returns structured JSON        │
│     - Works on ANY format            │
│     - Used when regex confidence     │
│       is low (< 70%)                 │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│  Step 3: Field Fusion & Normalization│
│  (merge results, normalize values)   │
│                                      │
│  - Merge regex + Gemini results      │
│  - Normalize amount (remove symbols, │
│    handle comma/dot decimal issues)  │
│  - Parse dates (multiple formats)    │
│  - Map bank names to standard names  │
│  - Calculate overall confidence      │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│  Step 4: Response                    │
│  Returns ReceiptParseResult JSON     │
│  → Frontend auto-fills the form     │
└──────────────────────────────────────┘
```

---

## Files to Create/Modify

### NEW FILES

| File | Purpose |
|---|---|
| `backend/ml/receipt_parser/__init__.py` | Package init, exports main parser function |
| `backend/ml/receipt_parser/ocr_engine.py` | OCR abstraction — tries easyocr → tesseract → paddleocr with fallback |
| `backend/ml/receipt_parser/bank_patterns.py` | Regex patterns for Pakistani banks (Meezan, HBL, Allied, UBL, SadayPay, Easypaisa, etc.) |
| `backend/ml/receipt_parser/field_extractor.py` | Generic regex-based field extraction (amount, date, account, names) |
| `backend/ml/receipt_parser/field_normalizer.py` | Normalize amounts, dates, bank names, currency codes |
| `backend/ml/receipt_parser/gemini_extractor.py` | Gemini API wrapper for AI-based extraction (moved from receipt.py) |
| `backend/ml/receipt_parser/parser.py` | Main parser orchestrator — combines regex + Gemini, fuses fields |

### MODIFIED FILES

| File | Changes |
|---|---|
| `backend/api/receipt.py` | Refactor to use `ml/receipt_parser/` module. Fix `io` import bug. Add better error handling |
| `backend/schemas/receipt.py` | Update `confidence` to be dynamically calculated, add `extraction_method` field |
| `backend/requirements.txt` | Add `pytesseract`, `paddleocr`, `opencv-python` as optional OCR backends |
| `frontend/src/pages/NewTransaction.jsx` | Add receipt preview thumbnail, show confidence badge, show which fields were auto-filled |

---

## Detailed Implementation Plan

### 1. `ocr_engine.py`
- `extract_text(image_bytes: bytes) -> str`
- Try easyocr first (already installed)
- Fallback to pytesseract (if installed)
- Fallback to paddleocr (if installed)
- Return raw OCR text

### 2. `bank_patterns.py`
- Dictionary of bank-specific regex patterns:
  - `meezen_patterns`: "Meezan Bank", account format `XXXX-XXXX-XXXXXXXXXX`, date format `DD-MMM-YYYY`
  - `hbl_patterns`: "Habib Bank", account format, specific transaction IDs
  - `allied_patterns`: "Allied Bank", specific formats
  - `ubl_patterns`: "UBL", specific formats
  - `sadaypay_patterns`: "SadayPay", digital wallet format
  - `easypaisa_patterns`: "Easypaisa", mobile wallet format
  - `generic_patterns`: Fallback for unknown formats
- Each bank has patterns for: amount, date, transaction ID, sender, receiver, account numbers

### 3. `field_extractor.py`
- `extract_fields(text: str, bank_name: str = None) -> dict`
- Detect bank from text using bank_patterns
- Apply bank-specific patterns
- Fallback to generic patterns (amount with currency symbol, date formats, account numbers)
- Return extracted fields with individual confidence scores per field

### 4. `field_normalizer.py`
- `normalize_amount(raw: str) -> float` — handles PKR, USD, Rs, commas, decimals
- `normalize_date(raw: str) -> datetime` — handles DD-MMM-YYYY, DD/MM/YYYY, M/D/Y, etc.
- `normalize_bank_name(raw: str) -> str` — maps variations to standard names
- `detect_currency(text: str) -> str` — detects from symbols (Rs, $, €) or text

### 5. `gemini_extractor.py`
- Refactored from existing `extract_fields_with_gemini()` in receipt.py
- Added timeout handling
- Added structured prompt for Pakistani bank receipts
- Added retry logic

### 6. `parser.py`
- `parse_receipt(image_bytes: bytes) -> ReceiptParseResult`
- Orchestrates: OCR → Field Extraction (regex) → Gemini (if confidence low) → Fusion → Normalization
- Calculates overall confidence based on how many required fields were extracted

---

## How It Handles Different Receipt Formats

| Bank/Format | Detection | Extraction Strategy |
|---|---|---|
| **Meezan Bank** | Detects "Meezan Bank Ltd" text | Specific regex for Meezan account format `XXXX-XXXX-XXXXXXXXXX` and date format |
| **Allied Bank** | Detects "Allied Bank" text | Specific patterns for Allied receipt layout |
| **HBL** | Detects "Habib Bank" or "HBL" | Specific patterns for HBL receipts |
| **UBL** | Detects "United Bank" or "UBL" | UBL-specific formats |
| **SadayPay** | Detects "SadayPay" | Digital wallet specific fields (mobile number, wallet ID) |
| **Easypaisa** | Detects "Easypaisa" | Mobile wallet formats |
| **Unknown format** | No bank detected | Generic regex + Gemini AI extraction |
| **Any format** | Always runs Gemini as enhancement | AI-based extraction understands context regardless of layout |

