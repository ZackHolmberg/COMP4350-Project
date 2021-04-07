import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    def __init__(self, serviceName):
        env_path = Path("" + serviceName) / ".env"
        print(env_path)
        load_dotenv(dotenv_path=env_path)
        # load the environment variables
        self.MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
        self.MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
        self.MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
        self.MONGODB_HOSTNAME = os.getenv("MONGODB_HOSTNAME")
        self.MONGO_URI = (
            "mongodb://"
            + self.MONGODB_USERNAME
            + ":"
            + self.MONGODB_PASSWORD
            + "@"
            + self.MONGODB_HOSTNAME
            + ":27017/"
            + self.MONGODB_DATABASE
            + "?authSource=admin"
        )
