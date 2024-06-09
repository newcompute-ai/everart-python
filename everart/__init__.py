from dotenv import load_dotenv
import os

from everart.client import Client

load_dotenv()

api_key = os.environ.get("EVERART_API_KEY")

default_client = Client(api_key=api_key)

v1 = default_client.v1