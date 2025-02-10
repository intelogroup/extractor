import streamlit as st
import PyPDF2
import io
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="PDF Reference Extractor")

st.title("PDF Reference Extractor")

def extract_pdf_info(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        first_page = pdf_reader.pages[0].extract_text()
        
        # Basic extraction (we'll improve this later)
        info = {
            'title': first_page.split('\n')[0],
            'authors': 'Not implemented',
            'year': 'Not implemented',
            'journal': 'Not implemented',
            'doi': 'Not implemented'
        }
        return info
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

# File upload
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for pdf_file in uploaded_files[:2]:  # Limit to 2 files
        st.write(f"Processing: {pdf_file.name}")
        
        info = extract_pdf_info(pdf_file)
        if info:
            st.write("Extracted Information:")
            for key, value in info.items():
                st.write(f"{key}: {value}")
            
            if st.button(f"Export to Google Sheets ({pdf_file.name})"):
                st.write("Google Sheets export not implemented yet")

st.sidebar.markdown("### About")
st.sidebar.write("Upload academic PDFs to extract bibliographic information.")
