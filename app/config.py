import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

GITHUB_API_URL = "https://api.github.com"

HOST: str = "0.0.0.0"
PORT: int = 8000
DEBUG: bool = True