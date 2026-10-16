import re
import streamlit as st
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer & Job Matcher")
st.caption("A local, transparent keyword-matching demo. Your resume stays in this app session.")

DEFAULT_SKILLS = [
    "python", "java", "c++", "sql", "javascript", "typescript", "react",
    "fastapi", "flask", "django", "machine learning", "deep learning",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "opencv",
    "nlp", "computer vision", "rest api", "docker", "aws", "azure",
    "git", "github", "postgresql", "mysql", "mongodb", "html", "css",
    "data analysis", "power bi", "excel", "communication", "problem solving"
]

def extract_resume(uploaded_file):
    if uploaded_file is None:
        return ""
    data = uploaded_file.getvalue()
    if uploaded_file.name.lower().endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

uploaded = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
resume_paste = st.text_area("Or paste resume text", height=180, placeholder="Paste resume text here...")
job_description = st.text_area("Job description", height=220, placeholder="Paste the job description here...")
skills_text = st.text_input("Skills to check (comma-separated)", value=", ".join(DEFAULT_SKILLS))

if st.button("Analyze match", type="primary"):
    try:
        resume = resume_paste.strip() or extract_resume(uploaded)
    except Exception as exc:
        st.error(f"Could not read the file: {exc}")
        st.stop()
    if not resume or not job_description.strip():
        st.warning("Add resume text/file and a job description first.")
        st.stop()

    skills = [s.strip() for s in skills_text.split(",") if s.strip()]
    resume_norm, job_norm = normalize(resume), normalize(job_description)
    relevant = [s for s in skills if normalize(s) in job_norm]
    matched = [s for s in relevant if normalize(s) in resume_norm]
    missing = [s for s in relevant if normalize(s) not in resume_norm]
    score = round(100 * len(matched) / len(relevant)) if relevant else 0

    left, right, third = st.columns(3)
    left.metric("Keyword match", f"{score}%")
    right.metric("Job skills identified", len(relevant))
    third.metric("Matched skills", len(matched))
    st.progress(score / 100)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("✅ Skills found")
        st.write(", ".join(matched) if matched else "No exact keyword matches found.")
    with c2:
        st.subheader("🎯 Skills to review")
        st.write(", ".join(missing) if missing else "All detected job keywords were found.")
    report = (
        f"AI Resume Analyzer Report\nKeyword match: {score}%\n"
        f"Job skills identified: {', '.join(relevant)}\n"
        f"Matched skills: {', '.join(matched)}\n"
        f"Skills to review: {', '.join(missing)}\n"
        "\nNote: This is a keyword-based estimate, not a hiring decision."
    )
    st.download_button("Download report", report, file_name="resume_analysis.txt")
