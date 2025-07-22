import google.generativeai as genai
import os
from dotenv import load_dotenv
from questions import questions

load_dotenv()

apiKey=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=apiKey)
model = genai.GenerativeModel("gemini-2.5-flash")

def select_best_questions(user_intro):
    prompt = f"""
You're a psychologist assistant. Based on the user's description below, pick the 5–6 most relevant questions from the following list:

User input: "{user_intro}"

Questions:
{questions}

Return only the selected questions as a list.
"""
    res = model.generate_content(prompt)
    return [line.strip("-•1234567890. ") for line in res.text.strip().split("\n") if line.strip()]
    
def generate_personality_profile(user_intro, qa_pairs):
    formatted_answers = "\n".join([f"{q} → {a}" for q, a in qa_pairs])

    prompt = f"""
You're a friendly psychologist. Based on the description and answers below, give a personality analysis.

User intro: "{user_intro}"

Answers:
{formatted_answers}

Generate a short and friendly personality profile.
"""
    res = model.generate_content(prompt)
    return res.text.strip()