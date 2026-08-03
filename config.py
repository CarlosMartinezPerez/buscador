import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gemini API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # SMTP / E-mail Settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "editais.db")
    
    # Target search topics
    SEARCH_QUERIES = [
        'edital "bolsa de estudo" "inteligência artificial" OR "machine learning" 2026 OR 2025',
        'edital "residência tecnológica" OR "capacitação" "sistemas embarcados" OR "IoT" bolsa',
        'edital "capacitação em TI" "desenvolvimento web" OR "software" bolsa 2026',
        'edital "bolsa de capacitação" Softex OR EMBRAPII OR MCTI TI',
        'edital "programa de residência" TI bolsa de estudo 2026'
    ]

    @classmethod
    def validate(cls):
        missing = []
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not cls.SMTP_USER:
            missing.append("SMTP_USER")
        if not cls.SMTP_PASSWORD:
            missing.append("SMTP_PASSWORD")
        if not cls.NOTIFY_EMAIL:
            missing.append("NOTIFY_EMAIL")
        return missing
