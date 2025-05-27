
from utils.search_resource import get_resource_links

def generate_roadmap(analysis):
    subskills = analysis["sub_skills"]
    timeframe = analysis.get("timeframe", "").strip().lower()
    
    weeks = 12
    
    try:
        number = int(timeframe.split()[0])
        if "month" or "months" in timeframe:
            weeks = number * 4
        elif "year" or "years" in timeframe:
            weeks = number * 52
        elif "weeks" in timeframe:
            weeks = number
    except (ValueError, IndexError):
        pass

    per_skill_weeks = max(1, weeks // max(1, len(subskills)))

    modules = []
    week_conter = 1
    for skill in subskills:
        links = get_resource_links(skill)
        if not links:
            links = [f"https://www.google.com/search?q={skill.replace(' ', '+')}"]
        
        modules.append({
            "week": f"Week: {week_conter}- {week_conter + per_skill_weeks - 1}",
            "topic": skill,
            "time":f"{4 * per_skill_weeks} hours",
            "resources": links

        })
        week_conter += per_skill_weeks
    roadmap = {
        "title": f"{analysis['learning_intent'].capitalize()} {analysis['main_skill']} ({analysis['proficiency_level'].capitalize()} Level)",
        "duration": analysis["timeframe"],
        "learning_style": analysis["learning_style"],
        "modules": modules
    }
    return roadmap

