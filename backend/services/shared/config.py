from dotenv import load_dotenv
from pathlib import Path
import os


class Config:
    def __init__(self):
        env_path = Path('./users') / '.env'
        load_dotenv(dotenv_path = env_path)
        print('env is : ')
        print(os.environ)
        #load the environment variables
        self.MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
        self.MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
        self.MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
        self.MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME')