load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def analyze_prompt(user_prompt):
    system_prompt = """ you are a AI assistant that analyzes user goals related to tech skills.
    your task is to extract:
    1. Main skill highlighted in the prompt
    2. Sub-skills related to the main skill
    3. learning intent (e.g., learning, improving, mastering)
    4. learning style (e.g., hands-on, theoretical, project-based)
    5.proficiency level (e.g., beginner, intermediate, advanced)
    Return a pytgon dictionary with the following keys
""" 
    full_prompt = system_prompt + "\n\nUser Prompt: " + user_prompt

    response = model.generate_content(full_prompt)
    
    try: 
        return eval(response.text)  # Convert the response string to a Python dictionary
    except Exception as e:
        return {
            "error": "Failed to parse the response",
            "details": str(e)
        }
    
# Example usage
if __name__ == "__main__":
    user_prompt = "I want to learn Python programming for data analysis and machine learning."
    result = analyze_prompt(user_prompt)
    print(result)