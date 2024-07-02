import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text

# Input prompt for the ATS task
input_prompt = """
Act as an expert-level Applicant Tracking System (ATS) with comprehensive knowledge across various tech fields, including software engineering, data science, data analysis, machine learning, big data engineering, DevOps, etc. Your task is to evaluate the provided resume based on the given job description. Keep in mind that the job market is highly competitive, and your evaluation should offer the best possible assistance for improving the resume. Assign a percentage match based on the job description and identify missing keywords with high accuracy.

Here is the structure for your response: 


  "JD Match": "%"

  "Relevant Keywords" : []

  "MissingKeywords": []

  "Profile Summary": ""

  "Tips to Improve" : ""


"""

## streamlit

st.title("Swarnim's ATS")
st.text("Find your Resume ATS Score")
jd = st.text_area("Drop the JD")
uploaded_file = st.file_uploader("Upload your Resume" , type = "pdf" , help = "Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
