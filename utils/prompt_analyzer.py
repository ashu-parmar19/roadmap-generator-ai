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
    system_prompt = """ you are a AI assistant that analyzes user goals related to tech skills.
    your task is to extract:
    1. Main skill highlighted in the prompt
    2. Sub-skills related to the main skill
    3. learning intent (e.g., learning, improving, mastering)
    4. learning style (e.g., hands-on, theoretical, project-based)
    5.proficiency level (e.g., beginner, intermediate, advanced)
    6.timeframe (e.g., 3 months, 6 weeks, 1 year)
    Return a python dictionary with the following keys
    
""" 
    full_prompt = f"{system_prompt}\n\nUser Prompt: {user_prompt}"

    response = model.generate_content(full_prompt)
    return extract_json(response.text)
    
    


# result = analyze_prompt("I want to learn Python programming for data analysis. I prefer hands-on projects and I'm a beginner. in about 3 months")
# print(result)


# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)

