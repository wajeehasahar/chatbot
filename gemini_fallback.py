import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ⚡ Fast model
model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(prompt):
    try:
        # 🎯 SHORT + FAST PROMPT CONTROL
        short_prompt = f"""
You are Medatiq Markets Chatbot.

Rules:
- Give SHORT answers (max 3-4 lines)
- Be clear and direct
- No long explanations
- Focus on Forex & Crypto only

User: {prompt}
"""

        response = model.generate_content(
            short_prompt,
            generation_config={
                "max_output_tokens": 80,   # 🔥 limit length
                "temperature": 0.5          # ⚡ faster + less random
            }
        )

        if response and hasattr(response, "text"):
            return response.text.strip()

        return "⚠️ Empty response from Gemini."

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"