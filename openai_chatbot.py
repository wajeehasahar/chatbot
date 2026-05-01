from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Medatiq Markets Chatbot."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)

        # 👇 VERY IMPORTANT
        if "insufficient_quota" in error_msg or "429" in error_msg:
            return "FALLBACK_TRIGGER"

        return f"❌ OpenAI Error: {error_msg}"