import json
from google import genai
from backend.config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are an AI assistant that analyzes GitHub issues. "
    "Return ONLY valid JSON matching the required schema. "
    "Do not include explanations, markdown, or extra text."
)

USER_PROMPT_TEMPLATE = """
Issue Title:
{title}

Issue Body:
{body}

Comments:
{comments}

Return a JSON object with:
- summary: one sentence
- type: bug | feature_request | documentation | question | other
- priority_score: number 1–5 with short justification
- suggested_labels: 2–3 GitHub labels
- potential_impact: user impact if bug, else "N/A"
"""


def _extract_json(text: str) -> dict:
    """
    Safely extract JSON from LLM output that may include markdown/code fences.
    """
    text = text.strip()

    
    if text.startswith("```"):
        text = text.split("```")[1]

    if text.lstrip().startswith("json"):
        text = text.lstrip()[4:].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON returned by Gemini:\n{text}")


def analyze_issue(issue_data: dict) -> dict:
    prompt = SYSTEM_PROMPT + "\n\n" + USER_PROMPT_TEMPLATE.format(
        title=issue_data["title"],
        body=issue_data["body"],
        comments="\n".join(issue_data["comments"]) or "No comments"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise Exception("Empty response from Gemini API")

    result = _extract_json(response.text)

    if "priority_score" in result:
        result["priority_score"] = str(result["priority_score"])


    return result
