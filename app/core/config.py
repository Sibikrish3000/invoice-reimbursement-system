from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Invoice Reimbursement System"
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    # Vector Store Settings
    VECTOR_STORE_PATH: str = "data/vector_store"
    
    # LLM Settings
    LLM_MODEL_NAME: str = "mistral-large-latest"
    EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"pdf", "zip"}
    
    # Chat Settings
    MAX_CHAT_HISTORY: int = 10
    
    class Config:
        case_sensitive = True

settings = Settings() 