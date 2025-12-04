import os
from dotenv import load_dotenv

load_dotenv()

print("URI:", os.getenv("NEO4J_URI"))
print("USER:", os.getenv("NEO4J_USERNAME"))
print("PASS:", os.getenv("NEO4J_PASSWORD"))
