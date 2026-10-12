import os
from pathlib import Path

SKILLS_DIR = Path.home() / ".agents" / "skills"

def list_skills():
    """Lists all available skill files in the skills directory."""
    if not SKILLS_DIR.exists():
        return []
    return [f.stem for f in SKILLS_DIR.glob("*.md") or SKILLS_DIR.glob("*.txt")]

def read_skill(skill_name):
    """Reads the content of a specific skill file."""
    skill_path = SKILLS_DIR / f"{skill_name}.md"
    if not skill_path.exists():
        skill_path = SKILLS_DIR / f"{skill_name}.txt"
    
    if not skill_path.exists():
        return f"Skill '{skill_name}' not found."
    
    return skill_path.read_text(encoding="utf-8")

def skills_prompt():
    """Returns a prompt string listing available skills."""
    skills = list_skills()
    if not skills:
        return "No custom skills available."
    return f"Available skills: {', '.join(skills)}. Use read_skill to load a skill's instructions."
