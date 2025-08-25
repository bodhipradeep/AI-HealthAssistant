from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    GROQ_API_KEY: Optional[str] = Field(..., env="GROQ_API_KEY")
    HF_API_KEY: Optional[str] = Field(..., env="HF_API_KEY")
    WEATHER_API_KEY: str = Field(None, env="WEATHER_API_KEY")
    
    # Model Configuration
    Llama_MODEL: str = Field("meta-llama/llama-4-maverick-17b-128e-instruct", env="PRIMARY_MODEL")
    
    # Server Configuration
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
