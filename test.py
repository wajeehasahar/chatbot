import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Available Gemini Models:\n")

for model in genai.list_models():
    print(model.name)