# GitHub Issue AI Assistant

## Description:

An AI-powered web application that analyzes GitHub issues and generates structured insights and a human-readable summary using Google Gemini (gemini-flash-latest).
This project helps developers quickly understand GitHub issues by automatically classifying them, assigning priority, suggesting labels, and explaining potential impact.

## Problem Statement:

GitHub issues often contain long, unstructured discussions that are difficult to quickly understand or categorize.
This project solves that by:

Automatically analyzing GitHub issues
Categorizing issue type (bug, feature, documentation, etc.)
Assigning priority with justification
Suggesting relevant labels
Estimating potential impact
All results are returned in machine-safe JSON.

## Overview:

The application performs the following steps:
Accepts a GitHub repository URL and issue number
Retrieves the issue title, description, and comments from GitHub
Analyzes the issue using an AI model
Produces a structured JSON summary
Displays the result in a lightweight web interface

## Technologies Used:

Python
FastAPI (backend service)
Streamlit (user interface)
GitHub REST API
Google Gemini Flash (AI model)
The technology choices were kept minimal to keep the project easy to run and understand.

## Repository Layout:

github-issue-ai/
│
├── backend/
│   ├── main.py 
│   ├── github_client.py
│   ├── llm.py
│   ├── schemas.py
│   └── config.py
│
├── frontend/
│   └── app.py
│
├── .env
├── requirements.txt
└── README.md

### Backend (FastAPI)

Fetches GitHub issue using GitHub REST API
Sends issue content to Gemini
Validates and sanitizes AI output
Exposes /analyze endpoint
Auto-generates Swagger UI

### Frontend (Streamlit)

Simple, clean UI
User inputs:
GitHub repository URL
Issue number (manually entered)

Displays:
Human-readable summary
Raw JSON output
Friendly error messages and loading states

## AI & Prompt Engineering:

Prompt Design

Uses a strict system prompt enforcing valid JSON only
Explicitly forbids:
Markdown
Explanations
Numbered arrays (e.g. 0: "label")
Missing commas or malformed objects
Schema is clearly defined and validated after generation

Model Used

Gemini Flash (gemini-flash-latest)
Chosen for:
Fast response time
Free-tier friendliness
Stable structured output when prompted correctly

## Edge Case Handling

Issues with no title or body
Very long issue descriptions
Empty or malformed LLM responses
GitHub API failures
Network or rate-limit errors

## Setup Instructions:

Step 1: Clone the Repository:
git clone https://github.com/your-username/github-issue-ai.git
cd github-issue-ai

Step 2: Create Virtual Environment
python -m venv venv
source venv/Scripts/activate   # Windows

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Set Environment Variables
Create a .env file:
GEMINI_API_KEY=your_gemini_api_key_here

## Running the Application:

Step 1: Install required packages
pip install fastapi uvicorn requests python-dotenv pydantic streamlit google-genai

Step 2: Configure environment variables
Create a .env file in the root directory and add:
GEMINI_API_KEY=your_gemini_api_key_here

Step 3: Start the backend service
uvicorn backend.main:app --reload
The backend will run at:
http://127.0.0.1:8000

Step 4: Start the frontend(Streamlit)
Open another terminal and run:
python -m streamlit run frontend/app.py
Then open:
http://localhost:8501

Step 5: API Usage

GET /analyze:

Query Parameters
repo_url – GitHub repository URL
issue_number – Issue number
Example:
http://127.0.0.1:8000/analyze?repo_url=https://github.com/fastapi/fastapi&issue_number=1

## Sample Input(How to use):

Open the Streamlit UI
Enter a GitHub repository URL
Repository URL: https://github.com/facebook/react
Issue Number: 1
Click Analyze Issue to view the generated summary.
View:
📝 Readable summary
🧾 Structured JSON result

## Output

The UI displays two sections:

Readable Summary:
A human-friendly explanation that highlights:
Issue type
Priority
Short summary
User impact
Suggested labels
This makes it easy to quickly understand the issue without reading raw JSON.

Analysis Result:
The raw structured JSON returned by the backend, which can be:
Copied directly using the built-in code viewer
Downloaded using a dedicated Download JSON button


## API Response Structure:

The backend returns a JSON response in the following format:
{
  "summary": "",
  "type": "",
  "priority_score": "",
  "suggested_labels": [],
  "potential_impact": ""
}

## Extra Features Added

In addition to the core requirements, a few small but thoughtful enhancements were included:

1.Readable Summary View
A human-readable summary is shown above the raw JSON to improve usability.

2.Basic UI Error Handling
Clear error messages are displayed when external APIs fail (e.g., GitHub rate limits or AI response issues).

3.Safe AI Response Parsing
The backend safely handles cases where the AI returns JSON wrapped in code blocks.

4.In-Memory Caching (Frontend)
Results for the same repository and issue number are cached during a session to avoid repeated API and AI calls.

5.Download JSON Button
A dedicated button allows downloading the analysis result as a JSON file.

## Submission Summary:

This project emphasizes robust prompt engineering to ensure consistent, valid JSON output from the AI.
The system is designed with clear separation of backend and frontend concerns, graceful error handling, and support for common edge cases.
Setup and execution are intentionally simple, allowing the entire application to run locally in under five minutes.
Additional UI and usability improvements were included to enhance clarity and developer experience.

## Additional Notes:

The application works only with public GitHub repositories
The AI model is used for summarization and categorization purposes
The free Gemini tier has limited usage, so excessive testing may hit rate limits

Thank you for reviewing this submission.
