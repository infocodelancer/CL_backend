import os
from dotenv import load_dotenv

# Load values from .env file into environment
load_dotenv()

class Settings:
    """
    Centralized app settings loaded from environment variables (.env).
    """

    # Flask
    ENV: str = os.getenv("FLASK_ENV", "production")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "0") == "1"

    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI")
    DB_NAME: str = os.getenv("DB_NAME")

    # Email (use Gmail App Password, not normal password)
    EMAIL_HOST: str = os.getenv("EMAIL_HOST")
    EMAIL_PORT: int = os.getenv("EMAIL_PORT")
    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASS: str = os.getenv("EMAIL_PASS")

    # Optional branding
    APP_BRAND_NAME: str = os.getenv("APP_BRAND_NAME", "Codelancer")
    APP_REPLY_TO: str = os.getenv("APP_REPLY_TO", EMAIL_USER)

    def validate(self):
        """
        Ensure required settings are present; raise error if missing.
        """
        missing = []
        if not self.MONGO_URI:
            missing.append("MONGO_URI")
        if not self.DB_NAME:
            missing.append("DB_NAME")
        if not self.EMAIL_USER:
            missing.append("EMAIL_USER")
        if not self.EMAIL_PASS:
            missing.append("EMAIL_PASS")

        if missing:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

settings = Settings()
settings.validate()
