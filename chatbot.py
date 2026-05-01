from google import genai
import os
from dotenv import load_dotenv
import time

# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key missing in .env file")
    exit()

# Create client
client = genai.Client(api_key=api_key)

system_prompt = """
You are Medatiq Markets Chatbot.
Help with Forex & Crypto.
"""

print("💹 Chatbot started... (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    bot_reply = "⚠️ Something went wrong."

    # Retry logic
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",  # lightweight model
                contents=system_prompt + "\nUser: " + user_input
            )

            if response and hasattr(response, "text"):
                bot_reply = response.text
            else:
                bot_reply = "⚠️ Empty response from API."

            break  # success

        except Exception as e:
            error_msg = str(e)

            if "429" in error_msg:
                print("⏳ Quota exceeded... waiting...")
                time.sleep(5)

            elif "503" in error_msg:
                print("🔄 Server busy... retrying...")
                time.sleep(3)

            else:
                bot_reply = f"❌ Error: {error_msg}"
                break

    print("Bot:", bot_reply)