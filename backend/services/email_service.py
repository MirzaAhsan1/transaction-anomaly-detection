import os
from pathlib import Path
from models import Transaction
import smtplib

from core.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

def send_transaction_email(transaction: Transaction, user_email: str):
    """
    Mock email service. In production, this would use smtplib to send via SMTP.
    """
    prediction = transaction.prediction
    
    if prediction == "Fraud":
        template_path = TEMPLATES_DIR / "fraud_alert.html"
        subject = f"SECURITY ALERT: Suspicious Transaction Detected ({transaction.transaction_id})"
    else:
        template_path = TEMPLATES_DIR / "normal_transaction.html"
        subject = f"Payment Successful: {transaction.transaction_id}"
        
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Very simple python string formatting
        # Using .replace instead of .format because HTML has { } in CSS.
        html_content = html_content.replace("{transaction_id}", str(transaction.transaction_id))
        html_content = html_content.replace("{currency}", str(transaction.currency))
        html_content = html_content.replace("{amount}", str(transaction.amount))
        html_content = html_content.replace("{merchant_name}", str(transaction.merchant_name))
        html_content = html_content.replace("{payment_method}", str(transaction.payment_method))
        html_content = html_content.replace("{transaction_time}", str(transaction.transaction_time))
        html_content = html_content.replace("{risk_score}", str(transaction.risk_score))
        html_content = html_content.replace("{confidence_score}", str(transaction.confidence_score))


        # Create email
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.smtp_from_email
        message["To"] = user_email

         # Plain text fallback


        if prediction == "Fraud":
            text_body = f"""
Suspicious Transaction Detected

Transaction ID : {transaction.transaction_id}
Amount         : {transaction.amount} {transaction.currency}
Merchant       : {transaction.merchant_name}

Our AI Fraud Detection System has detected unusual activity.

If this wasn't you, please secure your account immediately.
"""

        else:
            text_body = f"""
Payment Successful

Transaction ID : {transaction.transaction_id}
Amount         : {transaction.amount} {transaction.currency}
Merchant       : {transaction.merchant_name}

Your transaction was processed successfully.

No further action is required.
"""

        message.attach(MIMEText(text_body, "plain"))
        message.attach(MIMEText(html_content, "html"))

        # Connect to Gmail SMTP
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:

            server.starttls()

            server.login(
                settings.smtp_username,
                settings.smtp_password,
            )

            server.sendmail(
                settings.smtp_from_email,
                user_email,
                message.as_string(),
            )

        print(f"Transaction email sent successfully to {user_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
