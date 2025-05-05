from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Application configuration settings.
    
    Attributes:
        API_PREFIX: Prefix for all API endpoints
        SECRET_KEY: Secret key for security features
        DATABASE_URL: Connection string for the database
        CORS_ALLOW_ORIGINS:list[str] of allowed origins for CORS
        ALLOWED_HOSTS: list[str] of allowed hosts for CORS
        SERVER_NAME: Name identifier for the server
        PORT: Port number the server runs on
        HOST: Hostname the server binds to
    """
    # API settings
    API_PREFIX: str = "/api"
    
    # Database settings
    DATABASE_URL: str = ""
    
    # CORS and allowed hosts
    # CORS_ALLOWED_ORIGINS: list[str] = ["*"]
    # ALLOWED_HOSTS: list[str] = ["localhost","127.0.0.1"]
    
    # Server Information
    SERVER_NAME: str = "FastAPI Server"
    PORT: int = 8000
    HOST: str = "localhost"
    
    # Model API KEY
    GEMINI_API_KEY: str = os.environ.get
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = 'ignore'

# Create settings instance
settings = Settings()