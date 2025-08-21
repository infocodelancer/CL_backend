import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid
from config import settings


def build_email(to_email: str, subject: str, body: str) -> MIMEText:
    """
    Build a generic email message.
    """
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((settings.APP_BRAND_NAME, settings.EMAIL_USER))
    msg["To"] = to_email
    msg["Message-ID"] = make_msgid(domain="codelancer.local")
    if settings.APP_REPLY_TO:
        msg["Reply-To"] = settings.APP_REPLY_TO
    return msg


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email using SMTP.
    """
    try:
        msg = build_email(to_email, subject, body)
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        return True
    except Exception as e:
        print("Email sending failed:", e)
        return False


def send_confirmation_email(to_email: str, name: str) -> bool:
    """
    Send confirmation email to customer after registration.
    """
    brand = settings.APP_BRAND_NAME
    subject = f"Registration Successful — {brand}"
    body = f"""
Hi {name},

Thank you for registering with {brand}! 🎉  
We’re excited to have you on board.

Our team has received your details and we will review them shortly.  
One of our representatives will get in touch with you soon to guide you through the next steps.

If you have any questions in the meantime, feel free to reach out to us at {settings.APP_REPLY_TO}.

We look forward to working with you!

Best regards,  
Team {brand}
"""
    return send_email(to_email, subject, body)


def send_super_admin_notification(admin_email: str, customer: dict) -> bool:
    """
    Send new customer registration details to a super admin.
    """
    subject = f"New Registration - {customer.get('firstName')} {customer.get('lastName')}"
    body = f"""
Hello Admin,

A new customer has registered with the following details:

First Name: {customer.get('firstName')}
Last Name: {customer.get('lastName')}
Email: {customer.get('email')}
Phone: {customer.get('phone')}
Institution: {customer.get('institution')}
Course: {customer.get('course')}
Year: {customer.get('year')}
Project Type: {customer.get('projectType')}
Timeline: {customer.get('timeline')}
Project Description: {customer.get('projectDescription')}

Please review their details in the system.
"""
    return send_email(admin_email, subject, body)
