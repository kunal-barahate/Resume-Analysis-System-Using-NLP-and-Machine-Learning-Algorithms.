import google.generativeai as genai
import fitz  # PyMuPDF

# Set your Google Gemini Pro API Key
genai.configure(api_key="AIzaSyAgmZCT35RbzEpuAoahuz4EYI6-g1lIjR0")

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF resume."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def analyze_resume(resume_file, job_description):
    """Uses Google Gemini Pro to analyze the resume."""
    resume_text = extract_text_from_pdf(resume_file)

    prompt = f"""
    You are an ATS Resume Analyzer. Compare the following resume text with the given job description.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}

    Provide the following:
    1. Resume Match Score (percentage).
    2. Missing Keywords.
    3. Strengths and weaknesses of the resume.
    4. Suggestions to improve the resume.
    5. Job Suggestions.
    """

    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"