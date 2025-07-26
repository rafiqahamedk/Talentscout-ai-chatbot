import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use available models
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def generate_questions(tech_stack, experience):
    techs = [t.strip() for t in tech_stack.split(",") if t.strip()]
    all_questions = ""

    for tech in techs:
        prompt = (
            f"Generate 3 interview questions for a candidate with {experience} years of experience in {tech}. "
            "The questions should reflect their skill level and include real-world application where appropriate."
        )

        try:
            response = model.generate_content(prompt)
            questions = response.text
            all_questions += f"\n\n**{tech} Questions:**\n{questions}"
        except Exception as e:
            all_questions += f"\n\n**{tech} Questions:**\n(Error: {e})"

    return all_questions.strip()
