import json
import os
import re
from typing import Optional

import pymupdf as fitz
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field


load_dotenv()


# Pydantic Models
class Education(BaseModel):
    degree: str
    institution: str
    cgpa: Optional[float] = None
    graduation_year: Optional[int] = None


class Project(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    role: str
    organization: str
    description: str
    technologies: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    education: list[Education] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)


# Resume Section Detection
SECTION_NAMES = {
    "education": [
        "education",
        "academic background",
        "academics"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills"
    ],

    "certifications": [
        "certifications",
        "certificates"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
    ]
}


# pdf extraction
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    extract text from a pdf provided as bytes.
    """

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# text cleaning
def clean_text(text: str) -> str:
    """
    Normalize extracted resume text.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = "\n".join(
        line.strip()
        for line in text.split("\n")
    )

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# section detection
def detect_sections(text: str) -> dict[str, int]:
    """
    Detect known resume section headings.
    """

    sections = {}

    lines = text.splitlines()

    for index, line in enumerate(lines):

        normalized = line.lower().strip()

        for section, possible_names in SECTION_NAMES.items():

            if normalized in possible_names:
                sections[section] = index

    return sections


def extract_sections(
    text: str,
    section_positions: dict[str, int]
) -> dict[str, str]:

    lines = text.splitlines()

    sorted_sections = sorted(
        section_positions.items(),
        key=lambda x: x[1]
    )

    extracted = {}

    for index, (section_name, start_index) in enumerate(
        sorted_sections
    ):

        if index + 1 < len(sorted_sections):
            end_index = sorted_sections[index + 1][1]
        else:
            end_index = len(lines)

        content = lines[start_index + 1:end_index]

        extracted[section_name] = "\n".join(
            content
        ).strip()

    return extracted


# LLM context
def build_resume_context(
    sections: dict[str, str]
) -> str:

    context = ""

    for section_name, content in sections.items():

        context += (
            f"\n### {section_name.upper()}\n"
        )

        context += content
        context += "\n"

    return context


# LLM extraction
RESUME_EXTRACTION_PROMPT = """
You are a resume information extraction system.

Your task is to extract ALL factual information explicitly present in the provided resume and return it as a structured JSON object that exactly matches the CandidateProfile schema.

IMPORTANT:
- The CandidateProfile schema is the ONLY source of truth for the JSON structure.
- Use EXACTLY the field names defined in the schema.
- Never rename a field.
- Never create additional fields that are not present in the schema.
- Never use alternative field names.
- Do not return markdown, explanations, comments, or ```json fences.
- Return ONLY the JSON object.

GENERAL RULES:
1. Extract only information explicitly present in the resume.
2. Never invent, infer, assume, or hallucinate information.
3. Preserve the candidate's wording where appropriate.
4. Extract as much information as possible from the resume.
5. If a string field has no corresponding information, use "".
6. If a list field has no corresponding information, use [].
7. If a nullable field has no corresponding information, use null.
8. Do not omit required fields.
9. Do not add fields that are not defined in CandidateProfile.
10. Keep dates, names, organizations, technologies, links, and descriptions faithful to the resume.

SKILLS:
- Extract all explicitly listed technical and professional skills.
- Preserve individual skills as separate items when appropriate.
- Do not infer additional skills from projects or experience.
- Do not add a technology merely because it would normally be associated with a project.

EDUCATION:
- Extract every education entry.
- Extract the exact degree/program name.
- Extract the institution name.
- Extract CGPA only when explicitly mentioned.
- Extract graduation year only when explicitly mentioned.
- If CGPA or graduation year is absent, use null.

EXPERIENCE:
- Extract internships, jobs, work experience, research experience, and relevant organizational/professional experience.
- Keep each experience as a separate entry.
- Extract the exact role/title.
- Extract the organization/company name.
- Preserve the description of responsibilities and work.
- Extract technologies explicitly mentioned in that experience.
- Do not infer technologies.

PROJECTS:
- Extract EVERY project mentioned in the resume.
- Each project must use the field `name`, NOT `title`.
- Extract the project name exactly or as closely as possible to the resume.
- Extract the project's description.
- Extract technologies explicitly associated with that project.
- Do not infer technologies from the general skills section.
- If the resume contains project links but the CandidateProfile schema does not contain a field for them, do not create a new field for those links.
- Do not use fields such as `title`, `github`, `liveDemo`, `link`, or `url` unless those fields explicitly exist in CandidateProfile.

CERTIFICATIONS:
- Extract every explicitly mentioned certification.
- Preserve certification names accurately.

ACHIEVEMENTS:
- Extract every explicitly mentioned achievement, award, competition result, publication, recognition, or similar accomplishment that belongs in the achievements section.
- Do not convert ordinary responsibilities into achievements.

POSITIONS OF RESPONSIBILITY:
- Extract leadership roles, club positions, committee positions, student organization roles, and other explicitly stated positions of responsibility.
- Keep them separate from professional experience unless the schema indicates otherwise.

CONTACT INFORMATION:
- Extract the candidate's name exactly as written.
- Extract email, phone number, address, LinkedIn, GitHub, or other contact information ONLY if corresponding fields exist in CandidateProfile.
- Do not fabricate missing contact information.

SUMMARY:
- Extract the candidate's existing professional/profile summary if present.
- Do not write a new summary.
- Do not infer a summary from the resume if one is not explicitly provided.

CRITICAL PROJECT FIELD RULE:
If the CandidateProfile schema defines:
    "name"
then the JSON MUST contain:
    "name"

NEVER output:
    "title"

Similarly, use the exact field names from CandidateProfile for every other object and field.

The final response MUST be valid JSON and MUST conform to the CandidateProfile schema.

Resume:
"""


def extract_candidate_profile(
    resume_context: str
) -> CandidateProfile:

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    client = Groq(api_key=api_key)

    schema = CandidateProfile.model_json_schema()

    prompt = f"""
{RESUME_EXTRACTION_PROMPT}

Required JSON schema:

{json.dumps(schema, indent=2)}

Resume:

{resume_context}
"""

    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

    response_text = response.choices[0].message.content

    parsed_data = json.loads(response_text)

    return CandidateProfile.model_validate(
        parsed_data
    )


# parser pipeline
def parse_resume(
    file_bytes: bytes
) -> CandidateProfile:

    raw_text = extract_text_from_pdf(
        file_bytes
    )

    cleaned_text = clean_text(
        raw_text
    )

    section_positions = detect_sections(
        cleaned_text
    )

    sections = extract_sections(
        cleaned_text,
        section_positions
    )

    resume_context = build_resume_context(
        sections
    )

    candidate_profile = extract_candidate_profile(
        resume_context
    )

    return candidate_profile