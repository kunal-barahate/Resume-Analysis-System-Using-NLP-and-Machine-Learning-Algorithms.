import streamlit as st
import google.generativeai as genai
import pdfplumber
import time

# Set up Google Gemini Pro API
API_KEY = "AIzaSyAgmZCT35RbzEpuAoahuz4EYI6-g1lIjR0"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Function to extract text from an uploaded PDF resume
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to analyze resume using Google Gemini Pro
def analyze_resume(job_desc, resume_text, analysis_type):
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"""
    Analyze the following resume against this job description.
    Provide insights based on the selected analysis type: {analysis_type}.
    
    Also, provide an *ATS score (0-100)* based on how well the resume matches the job description.

   

    Job Description:
    {job_desc}

    Resume:
    {resume_text}
    """

    response = model.generate_content(prompt)
    return response.text

# Function to generate an AI-optimized resume
def generate_optimized_resume(resume_text):
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"""
    Improve this resume for better ATS compatibility.
    Ensure it is optimized for readability, keywords, and professional structure.

    Resume:
    {resume_text}
    """

    response = model.generate_content(prompt)
    return response.text

# Streamlit UI Configuration
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Custom CSS for UI/UX Improvements
st.markdown("""
    <style>
        /* Smooth Fade-in Animation */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        .fade-in {
            animation: fadeIn 2s ease-in-out;
        }
        
        /* Stylish Buttons */
        .stButton > button {
            width: 100%;
            background-color: #008CBA;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #005f73;
        }
        
        /* Glassmorphism Style for Cards */
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            animation: fadeIn 2s ease-in-out;
        }

        /* Loading Spinner Animation */
        @keyframes spin {
            from {transform: rotate(0deg);}
            to {transform: rotate(360deg);}
        }
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #008CBA;
            animation: spin 1s linear infinite;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Resume Analysis"])

# Home Page
if page == "🏠 Home":
    st.title("📄 Real-Time Resume Analyzer")
    st.markdown("<div class='fade-in'>🔍 Optimize your resume for ATS & improve your chances of getting hired!</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        job_desc = st.text_area("📝 Enter Job Description")
        resume = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
        
        if st.button("Next ➡"):
            if job_desc and resume:
                with st.spinner("🔄 Processing resume..."):
                    resume_text = extract_text_from_pdf(resume)
                    st.session_state["job_desc"] = job_desc
                    st.session_state["resume_text"] = resume_text
                    time.sleep(2)
                st.success("✅ Resume Uploaded Successfully!")
            else:
                st.warning("⚠ Please enter job description and upload a resume.")
        st.markdown("</div>", unsafe_allow_html=True)

# Resume Analysis Page
elif page == "📊 Resume Analysis":
    st.title("📊 Resume Analysis")
    
    if "job_desc" not in st.session_state or "resume_text" not in st.session_state:
        st.warning("⚠ Please go back to the Home page and upload a resume first.")
    else:
        st.subheader("✅ Job Description")
        st.write(st.session_state["job_desc"])
        st.subheader("📄 Uploaded Resume")
        st.write("Resume uploaded successfully. Ready for analysis!")

        # Feature Selection Dropdown
        analysis_type = st.selectbox("🔍 Choose Analysis Type", [
            "📈 Match Score", "❌ Missing Keywords", "💡 Skill Suggestions",
            "📝 AI-Powered Resume Feedback", "📥 Download Optimized Resume",
            "✅ Bullet Point Suggestions", "🚀 Skill Gap Analysis", "✅ Job Suggestion"
        ])

        # Run Analysis Button
        if st.button("🚀 Run Analysis"):
            with st.spinner("🔄 Analyzing resume..."):
                time.sleep(2)
                result = analyze_resume(st.session_state["job_desc"], st.session_state["resume_text"], analysis_type)
            
            st.success("✅ Analysis Complete!")
            st.markdown(f"<div class='card'>{result}</div>", unsafe_allow_html=True)

        # AI-Optimized Resume Download Button
        if analysis_type == "📥 Download Optimized Resume":
            if st.button("📥 Generate Optimized Resume"):
                with st.spinner("🔄 Generating AI-optimized resume..."):
                    time.sleep(3)
                    optimized_resume = generate_optimized_resume(st.session_state["resume_text"])
                st.success("✅ AI-Optimized Resume Ready!")
                st.download_button("⬇ Download Optimized Resume", optimized_resume, file_name="Optimized_Resume.txt")