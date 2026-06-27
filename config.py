import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = "my_secret_key"

    # MySQL
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "ai_repository_db"

    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")