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
        start = text.find('{')
        end = text.rfind('}') + 1
        cleaned = text[start:end]
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": "Failed to parse JSON",
            "details": str(e),
            "raw_output": text
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


    # Fallback/default
    result = {
        "skills": {},
        "intent": "",
        "style": "",
        "proficiency": "",
        "timeframe": ""
    }

    if isinstance(data, dict):
        for key in result:
            result[key] = data.get(key, result[key])

        # Ensure subskills are valid lists
        for skill in list(result["skills"].keys()):
            subskills = result["skills"][skill]
            if not isinstance(subskills, list):
                result["skills"][skill] = []
    else:
        result["error"] = "Model did not return valid structured output"

    return result
    
    




