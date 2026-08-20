from app.services.resume_parser import (
    clean_text,
    detect_sections,
)


def test_clean_text():

    text = "Hello   World\n\n\nPython"

    result = clean_text(text)

    assert result == "Hello World\n\nPython"


def test_detect_sections():

    text = """
SKILLS

Python, SQL

EDUCATION

B.Tech CSE

PROJECTS

Movie Recommendation
"""

    sections = detect_sections(text)

    assert "skills" in sections
    assert "education" in sections
    assert "projects" in sections