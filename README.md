# AI Resume Analyzer & Job Matcher

A local web app that extracts text from a resume and compares it with a job description using transparent keyword matching.

## Features
- Upload PDF or TXT resumes, or paste resume text.
- Paste a job description.
- Calculates a simple skills-match percentage.
- Shows matched and missing skills.
- Includes a downloadable plain-text analysis report.
- Runs locally; no resume is sent to a third-party API.

## Tech stack
Python, Streamlit, PyPDF, Pandas.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in your terminal.

## Notes
This is a portfolio/demo tool, not an automated hiring decision system. Matching is keyword-based and can miss synonyms or context. Review results manually.
