import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from pydantic import SecretStr, StrictStr

load_dotenv()

class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv('SITE_API', None)
    host_api: SecretStr = os.getenv('HOST_API', None)

