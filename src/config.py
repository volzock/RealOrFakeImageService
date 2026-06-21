import os


class Config:

    DATABASE_URL: str  = os.environ["DATABASE_URL"]
    REDIS_URL: str = os.environ["REDIS_URL"]
    MODEL_PATH: str  = os.environ["MODEL_PATH"]

    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8080"))