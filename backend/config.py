# Email configuration for password reset OTP
import os

# Gmail SMTP configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "aaaaditya82@gmail.com"
SMTP_PASSWORD = "tmns traq kkvo tbct"  # App password (with spaces as provided)
SMTP_FROM_EMAIL = "aaaaditya82@gmail.com"
SMTP_FROM_NAME = "AI Career Guidance System"

# OTP settings
OTP_EXPIRY_MINUTES = 10
OTP_LENGTH = 6

# Email content
EMAIL_SUBJECT = "Password Reset OTP - AI Career Guidance System"
EMAIL_BODY_TEMPLATE = """
Hello,

You have requested to reset your password for the AI Career Guidance System.

Your OTP code is: {otp_code}

This OTP will expire in {expiry_minutes} minutes.

If you did not request this password reset, please ignore this email.

Best regards,
AI Career Guidance Team
"""