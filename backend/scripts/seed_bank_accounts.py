"""Seed demo bank accounts into the database.

Fixes import issues when running as a script from within backend/.
"""

import sys
from pathlib import Path

# Ensure `db` and `models` are importable when executed as:
#   python scripts/seed_bank_accounts.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.session import SessionLocal
from models.bank_account import BankAccount


accounts = [
    {
        "account_number": "100000001",
        "account_holder_name": "Ali Khan",
        "bank_name": "HBL",
        "account_type": "Savings",
        "balance": 250000,
        "status": "Active",
    },
    {
        "account_number": "100000002",
        "account_holder_name": "Sara Ahmed",
        "bank_name": "Meezan Bank",
        "account_type": "Current",
        "balance": 98000,
        "status": "Active",
    },
    {
        "account_number": "100000003",
        "account_holder_name": "Ahmed Raza",
        "bank_name": "UBL",
        "account_type": "Savings",
        "balance": 72000,
        "status": "Active",
    },
    {
        "account_number": "100000004",
        "account_holder_name": "Ayesha Fatima",
        "bank_name": "MCB",
        "account_type": "Current",
        "balance": 145000,
        "status": "Active",
    },
    {
        "account_number": "100000005",
        "account_holder_name": "Muhammad Bilal",
        "bank_name": "Allied Bank",
        "account_type": "Savings",
        "balance": 320000,
        "status": "Active",
    },
    {
        "account_number": "100000006",
        "account_holder_name": "Zainab Bibi",
        "bank_name": "Bank Alfalah",
        "account_type": "Current",
        "balance": 15000,
        "status": "Inactive",
    },
    {
        "account_number": "100000007",
        "account_holder_name": "Usman Tariq",
        "bank_name": "Faysal Bank",
        "account_type": "Savings",
        "balance": 850000,
        "status": "Active",
    },
    {
        "account_number": "100000008",
        "account_holder_name": "Fatima Noor",
        "bank_name": "Askari Bank",
        "account_type": "Current",
        "balance": 45000,
        "status": "Active",
    },
    {
        "account_number": "100000009",
        "account_holder_name": "Hamza Ali",
        "bank_name": "Bank Al Habib",
        "account_type": "Savings",
        "balance": 1200000,
        "status": "Active",
    },
    {
        "account_number": "100000010",
        "account_holder_name": "Mariam Khan",
        "bank_name": "Habib Metropolitan",
        "account_type": "Current",
        "balance": 63000,
        "status": "Active",
    },
    {
        "account_number": "100000011",
        "account_holder_name": "Zeeshan Ahmed",
        "bank_name": "HBL",
        "account_type": "Current",
        "balance": 520000,
        "status": "Active",
    },
    {
        "account_number": "100000012",
        "account_holder_name": "Sana Mustafa",
        "bank_name": "Meezan Bank",
        "account_type": "Savings",
        "balance": 74000,
        "status": "Active",
    },
    {
        "account_number": "100000013",
        "account_holder_name": "Omer Khalid",
        "bank_name": "UBL",
        "account_type": "Current",
        "balance": 310000,
        "status": "Active",
    },
    {
        "account_number": "100000014",
        "account_holder_name": "Anum Jahangir",
        "bank_name": "MCB",
        "account_type": "Savings",
        "balance": 89000,
        "status": "Inactive",
    },
    {
        "account_number": "100000015",
        "account_holder_name": "Farhan Saeed",
        "bank_name": "Allied Bank",
        "account_type": "Current",
        "balance": 415000,
        "status": "Active",
    },
    {
        "account_number": "100000016",
        "account_holder_name": "Hina Yousaf",
        "bank_name": "Bank Alfalah",
        "account_type": "Savings",
        "balance": 1050000,
        "status": "Active",
    },
    {
        "account_number": "100000017",
        "account_holder_name": "Asad Mahmood",
        "bank_name": "Faysal Bank",
        "account_type": "Current",
        "balance": 23000,
        "status": "Active",
    },
    {
        "account_number": "100000018",
        "account_holder_name": "Khadija Rehman",
        "bank_name": "Askari Bank",
        "account_type": "Savings",
        "balance": 185000,
        "status": "Active",
    },
    {
        "account_number": "100000019",
        "account_holder_name": "Haris Bin Tariq",
        "bank_name": "Bank Al Habib",
        "account_type": "Current",
        "balance": 670000,
        "status": "Active",
    },
    {
        "account_number": "100000020",
        "account_holder_name": "Amna Sheikh",
        "bank_name": "Habib Metropolitan",
        "account_type": "Savings",
        "balance": 39000,
        "status": "Suspended",
    },
    {
        "account_number": "100000021",
        "account_holder_name": "Nabeel Qureshi",
        "bank_name": "HBL",
        "account_type": "Savings",
        "balance": 1450000,
        "status": "Active",
    },
    {
        "account_number": "100000022",
        "account_holder_name": "Sadia Iqbal",
        "bank_name": "Meezan Bank",
        "account_type": "Current",
        "balance": 220000,
        "status": "Active",
    },
    {
        "account_number": "100000023",
        "account_holder_name": "Faisal Shah",
        "bank_name": "UBL",
        "account_type": "Savings",
        "balance": 12500,
        "status": "Inactive",
    },
    {
        "account_number": "100000024",
        "account_holder_name": "Sidra Batool",
        "bank_name": "MCB",
        "account_type": "Current",
        "balance": 510000,
        "status": "Active",
    },
    {
        "account_number": "100000025",
        "account_holder_name": "Waqas Anwar",
        "bank_name": "Allied Bank",
        "account_type": "Savings",
        "balance": 95000,
        "status": "Active",
    },
    {
        "account_number": "100000026",
        "account_holder_name": "Kiran Naz",
        "bank_name": "Bank Alfalah",
        "account_type": "Current",
        "balance": 340000,
        "status": "Active",
    },
    {
        "account_number": "100000027",
        "account_holder_name": "Bilal Siddiqui",
        "bank_name": "Faysal Bank",
        "account_type": "Savings",
        "balance": 88000,
        "status": "Active",
    },
    {
        "account_number": "100000028",
        "account_holder_name": "Mahreen Gillani",
        "bank_name": "Askari Bank",
        "account_type": "Current",
        "balance": 120000,
        "status": "Active",
    },
    {
        "account_number": "100000029",
        "account_holder_name": "Arsalan Baig",
        "bank_name": "Bank Al Habib",
        "account_type": "Savings",
        "balance": 3100000,
        "status": "Active",
    },
    {
        "account_number": "100000030",
        "account_holder_name": "Tayyaba Malik",
        "bank_name": "Habib Metropolitan",
        "account_type": "Current",
        "balance": 412000,
        "status": "Active",
    },
    {
        "account_number": "100000031",
        "account_holder_name": "Kamran Akmal",
        "bank_name": "HBL",
        "account_type": "Current",
        "balance": 55000,
        "status": "Active",
    },
    {
        "account_number": "100000032",
        "account_holder_name": "Rabia Basri",
        "bank_name": "Meezan Bank",
        "account_type": "Savings",
        "balance": 615000,
        "status": "Active",
    },
    {
        "account_number": "100000033",
        "account_holder_name": "Imran Shafi",
        "bank_name": "UBL",
        "account_type": "Current",
        "balance": 190000,
        "status": "Active",
    },
    {
        "account_number": "100000034",
        "account_holder_name": "Jaweria Khan",
        "bank_name": "MCB",
        "account_type": "Savings",
        "balance": 28000,
        "status": "Inactive",
    },
    {
        "account_number": "100000035",
        "account_holder_name": "Adeel Chaudhry",
        "bank_name": "Allied Bank",
        "account_type": "Current",
        "balance": 780000,
        "status": "Active",
    },
    {
        "account_number": "100000036",
        "account_holder_name": "Sumaira Jamil",
        "bank_name": "Bank Alfalah",
        "account_type": "Savings",
        "balance": 430000,
        "status": "Active",
    },
    {
        "account_number": "100000037",
        "account_holder_name": "Zubair Hashmi",
        "bank_name": "Faysal Bank",
        "account_type": "Current",
        "balance": 165000,
        "status": "Active",
    },
    {
        "account_number": "100000038",
        "account_holder_name": "Nida Yasir",
        "bank_name": "Askari Bank",
        "account_type": "Savings",
        "balance": 920000,
        "status": "Active",
    },
    {
        "account_number": "100000039",
        "account_holder_name": "Saad Rafique",
        "bank_name": "Bank Al Habib",
        "account_type": "Current",
        "balance": 35000,
        "status": "Active",
    },
    {
        "account_number": "100000040",
        "account_holder_name": "Saba Qamar",
        "bank_name": "Habib Metropolitan",
        "account_type": "Savings",
        "balance": 2400000,
        "status": "Active",
    },
    {
        "account_number": "100000041",
        "account_holder_name": "Fahad Mustafa",
        "bank_name": "HBL",
        "account_type": "Savings",
        "balance": 1850000,
        "status": "Active",
    },
    {
        "account_number": "100000042",
        "account_holder_name": "Amina Jahanzeb",
        "bank_name": "Meezan Bank",
        "account_type": "Current",
        "balance": 135000,
        "status": "Active",
    },
    {
        "account_number": "100000043",
        "account_holder_name": "Taimoor Ali",
        "bank_name": "UBL",
        "account_type": "Savings",
        "balance": 8000,
        "status": "Suspended",
    },
    {
        "account_number": "100000044",
        "account_holder_name": "Noreen Akhter",
        "bank_name": "MCB",
        "account_type": "Current",
        "balance": 290000,
        "status": "Active",
    },
    {
        "account_number": "100000045",
        "account_holder_name": "Sohail Ahmed",
        "bank_name": "Allied Bank",
        "account_type": "Savings",
        "balance": 54000,
        "status": "Active",
    },
    {
        "account_number": "100000046",
        "account_holder_name": "Bushra Ansari",
        "bank_name": "Bank Alfalah",
        "account_type": "Current",
        "balance": 990000,
        "status": "Active",
    },
    {
        "account_number": "100000047",
        "account_holder_name": "Salman Saqib",
        "bank_name": "Faysal Bank",
        "account_type": "Savings",
        "balance": 115000,
        "status": "Active",
    },
    {
        "account_number": "100000048",
        "account_holder_name": "Zoya Nasir",
        "bank_name": "Askari Bank",
        "account_type": "Current",
        "balance": 460000,
        "status": "Active",
    },
    {
        "account_number": "100000049",
        "account_holder_name": "Hamza Abbasi",
        "bank_name": "Bank Al Habib",
        "account_type": "Savings",
        "balance": 3500000,
        "status": "Active",
    },
    {
        "account_number": "100000050",
        "account_holder_name": "Momal Sheikh",
        "bank_name": "Habib Metropolitan",
        "account_type": "Current",
        "balance": 71000,
        "status": "Active",
    },
]

def seed_accounts() -> None:
    db = SessionLocal()
    try:
        for account in accounts:
            exists = (
                db.query(BankAccount)
                .filter(
                    BankAccount.account_number == account["account_number"]
                )
                .first()
            )

            if not exists:
                db.add(BankAccount(**account))

        db.commit()
        print("Dummy accounts inserted successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_accounts()

