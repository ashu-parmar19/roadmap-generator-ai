import os
import google.generativeai as genai
from dotenv import load_dotenv
import re
import json


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def extract_json(text):
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("No JSON-like structure found in the text.")
    except Exception as e:
        return {
            "error": "Failed to parse the response",
            "details": str(e)
        }

def analyze_prompt(user_prompt):
    system_prompt = """
You are an AI assistant that extracts structured learning information from user prompts.

Return ONLY a Python dictionary in JSON format with the following structure:
{
  "skills": {
    "MainSkill1": ["Subskill1", "Subskill2", "Subskill3"],
    "MainSkill2": ["Subskill1", "Subskill2"]
  },
  "intent": "learning / mastering / improving",
  "style": "hands-on / theoretical / project-based / mixed",
  "proficiency": "beginner / intermediate / advanced",
  "timeframe": "3 months / 6 weeks / etc"
}

IMPORTANT:
- Do not include extra text.
- Make sure every skill has at least 2-3 realistic subskills.
- The entire output MUST be valid JSON.
"""


    full_prompt = f"{system_prompt}\n\nUser Prompt: {user_prompt}"

    response = model.generate_content(full_prompt)
    return extract_json(response.text)
    
    


result = analyze_prompt("I want to learn Python programming for data analysis. I prefer hands-on projects and I'm a beginner. in about 3 months")
print(result)


for m in genai.list_models():
    print(m.name, m.supported_generation_methods)

