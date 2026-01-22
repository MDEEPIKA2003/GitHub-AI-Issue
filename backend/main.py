from fastapi import FastAPI, HTTPException

from backend.github_client import fetch_issue
from backend.llm import analyze_issue
from backend.schemas import IssueAnalysis

app = FastAPI(title="GitHub Issue AI Assistant")

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/analyze", response_model=IssueAnalysis)
def analyze(repo_url: str, issue_number: int):
    try:
        issue_data = fetch_issue(repo_url, issue_number)
        analysis = analyze_issue(issue_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
