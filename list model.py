import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent / ".env", override=True)
client = OpenAI()

for m in client.models.list().data:
    print(m.id)