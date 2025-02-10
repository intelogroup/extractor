import streamlit as st
import subprocess
import sys

def install_pkgs():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])

install_pkgs()

import pdfplumber
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def analyze_with_gemini(text):
    prompt = """Analyze this academic text and extract as JSON:
    1. Title
    2. Authors
    3. Year
    4. Abstract
    5. Keywords
    6. Main findings
    
    Text: {text}"""
    
    try:
        response = model.generate_content(prompt.format(text=text))
        return response.text
    except Exception as e:
        st.error(f"Gemini API Error: {str(e)}")
        return None

def main():
    st.title("AI-Powered PDF Analyzer")
    
    uploaded_file = st.file_uploader("Upload academic PDF", type="pdf")
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        
        with st.spinner('Processing PDF...'):
            try:
                text = extract_text(uploaded_file)
                
                with col1:
                    st.subheader("Extracted Text")
                    st.text_area("", text[:1000] + "...", height=300)
                
                analysis = analyze_with_gemini(text)
                
                with col2:
                    st.subheader("AI Analysis")
                    if analysis:
                        st.json(analysis)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
