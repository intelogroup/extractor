import streamlit as st
import pdfplumber
import pandas as pd
import os
import json
from datetime import datetime

st.set_page_config(page_title="PDF Text Extractor")

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def save_to_csv(texts):
    df = pd.DataFrame({'timestamp': [datetime.now()], 'text': [texts]})
    df.to_csv('extracted_text.csv', index=False)
    return df

def main():
    st.title("PDF Text Extractor")
    
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    
    if uploaded_file:
        with st.spinner('Processing PDF...'):
            try:
                text = extract_text(uploaded_file)
                st.success("Text extracted successfully!")
                
                with st.expander("View Extracted Text"):
                    st.text_area("", text, height=300)
                    
                if st.button("Save to CSV"):
                    df = save_to_csv(text)
                    st.success("Saved to CSV!")
                    st.dataframe(df)
                    
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main()
