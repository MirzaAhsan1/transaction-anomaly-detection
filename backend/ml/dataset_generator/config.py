from datetime import datetime

# ==========================================
# Dataset Configuration
# ==========================================

TOTAL_TRANSACTIONS = 150_000
FRAUD_PERCENTAGE = 0.015  # 1.5%

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 12, 31)

# ==========================================
# Transaction Values
# ==========================================

MIN_AMOUNT = 5
MAX_AMOUNT = 10000

# ==========================================
# Currencies
# ==========================================

CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "PKR",
    "CAD",
    "AUD",
]

# ==========================================
# Transaction Types
# ==========================================

TRANSACTION_TYPES = [
    "Transfer",
    "Purchase",
    "Withdrawal",
    "Deposit",
]

# ==========================================
# Payment Methods
# ==========================================

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "Bank Transfer",
    "Mobile Wallet",
]

# ==========================================
# Merchant Categories
# ==========================================

MERCHANT_CATEGORIES = [
    "Retail",
    "Food",
    "Electronics",
    "Travel",
    "Healthcare",
    "Entertainment",
    "Utilities",
    "Education",
]

# ==========================================
# Banks
# ==========================================

BANKS = [
    "Chase",
    "Bank of America",
    "Wells Fargo",
    "Citibank",
    "HSBC",
    "Habib Bank",
    "Meezan Bank",
    "Allied Bank",
]

# ==========================================
# Browsers
# ==========================================

BROWSERS = [
    "Chrome",
    "Firefox",
    "Edge",
    "Safari",
]

# ==========================================
# Operating Systems
# ==========================================

OPERATING_SYSTEMS = [
    "Windows",
    "Linux",
    "macOS",
    "Android",
    "iOS",
]

# ==========================================
# Device Types
# ==========================================

DEVICE_TYPES = [
    "Desktop",
    "Mobile",
    "Tablet",
]

# ==========================================
# Languages
# ==========================================

LANGUAGES = [
    "en-US",
    "en-GB",
]

# ==========================================
# Timezones
# ==========================================

TIMEZONES = [
    "UTC",
    "Asia/Karachi",
    "America/New_York",
    "Europe/London",
]