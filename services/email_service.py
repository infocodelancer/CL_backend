import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid
from config import settings

def build_confirmation_email(to_email: str, name: str) -> MIMEText:
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


    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((brand, settings.EMAIL_USER))
    msg["To"] = to_email
    msg["Message-ID"] = make_msgid(domain="codelancer.local")
    if settings.APP_REPLY_TO:
        msg["Reply-To"] = settings.APP_REPLY_TO
    return msg

def send_email(msg: MIMEText) -> bool:
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        return True
    except Exception as e:
        # In production, use proper logging
        print("Email sending failed:", e)
        return False

def send_confirmation_email(to_email: str, name: str) -> bool:
    msg = build_confirmation_email(to_email, name)
    return send_email(msg)
