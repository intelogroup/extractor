import streamlit as st
import PyPDF2
import json
import os
from datetime import datetime
from sheets_manager import init_sheets_client, export_to_sheet, batch_export
from pdf_processor import extract_pdf_info

def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def validate_spreadsheet_id(id_str):
    return bool(id_str and len(id_str) == 44 and '/' not in id_str)

def save_credentials():
    try:
        credentials = {
            "type": "service_account",
            "project_id": "gen-lang-client-0224447803",
            "private_key_id": "6760123191313ec477724a36fd9bd192da45a5fe",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDUdwDj4hHO67uq\ntgXXfCPIgtXljkWvvUIPvUADE3a+SJ/cD7/0X747yQ4JWGRIzrvxB9wFp7yb0p6U\nydv/IbqJOlEjQ8NOdKumXEtkAIRjFxs7FkDQto7RaCIHar5r/yMOiuZDFstQmXNS\nftJMsLo/i05EH5OZ/pn+6ODmnP1/hUsUlk0NltvWr02tq3E/gqTZHrXc6/JvXswV\nHqkzACyg3/ygRIxtaSiYEj2f73cxj2H7IWl+Gh8MESZEicTNOL6Nk3KrwVBDEkL1\n87bOLQPPZNI115FWQ6iVYRocfWBcWgxrUHCd7WIJBDi9p+UdnY6QC/EcGB1g2U2U\n9IKOup3/AgMBAAECggEAJhKtNijsyAe2OYEkytiUEPphGiHEmxlvHSLstaBnRvH8\ns5Ke80u060G8IjCUx/dD9o1SADFuuv2jLUZ/BdkldDHfGFKsTQLbP5SKbgEpuBgL\n6SqzsrMEJMJkVq/qL7AouBJr8NnE1UyqPb48MUH6Hij4fXyrFo1pSySwKKM5SgBl\nLH2/DglGe7Jf9Xwn3SnIpzVdSlmHmautXRHBMuGo71Cw+ZukisjdixBD1+lpMrA+\npLptbt6pKYfGetFxrWQb0cF1bAt0Ldp/WUtyJyKvdCa+yCHAnF+eCRBcK5vF1a+T\nAoO9mmCGEUUiFlTgUnRlkudbLv+cOI0w/yPyhp/pAQKBgQDy320cMyQoHdY2RPYX\nu1Bc/02wqXpuWVreMxGvGSQLJr8pmVtZG6INaHgEVxubImHpB4Hq1y5SLPQhfl3P\ncg9GNCv0niTtmhljRrLCtu09uwE1MzdNoRZrGFKy8S43CDfJaJpqpDe6Zs0GwKhN\nSPVqoh5p6stiUlXZ5ZLdiR2S+wKBgQDf8tSJL14GnzHGUni4h0ypIxoqLV2X5Xbf\nCzmoYwpClt3aebsz4HuW6j6FI5GRgbfoGiOiBji0R2BU74DJb50P8CJHWZ/eRZm4\nMMMlNi883MyHwnCkApl7YYnBPZ7/yvKjk04WD1/YxYvfxsljWtT1CNmwjuJ1eQh5\nsbcO0ZfRzQKBgQDklijpa7DSGRLuTQWZ3HCMtrV2Wmyiw3LkwwgX1v+3hyZQjsgN\nHBbvq62Z2CphXoDshGZgk1pDeY/knjzI7D84Ag6E0vtKrcjLSVUiMm0jtogyfBvG\n8qBY97GOPbUTkqZ+5/a9/AV/aRX7DwTYiJyDWkZpxdTam0e2J36NB2pQVQKBgGrJ\nDZNEpN8fdcqNdMb4rRNRi55k92YAosgEQEAMyc2qxqrwtNUty4DQvXMa3MS3SAxC\nuo79zHgaONMHSS/EKu54oL/I+rQwF/Z+Oe86gRfSaSyrCK8MFkeA4QDl8zUhfsWE\n7g0S0683s1THIyxfGYCl8beAyncdeW8d0J4eTvhZAoGAO0q6r9z/BWrBnmAXObDZ\nI9EETsnHCNrHFJcv7HStvGmNLmP2DA/asj492jfxIT9ZZSYoEByKDWFgNcsbArb0\ncYCSBiWnS6UKTz7xnu0EApPptv4Ze0pEEL2eeh8Kie24fXYZ7ckfo8Ats37vE8Ew\nCdd75UxbfpB+uDwItkm8/Cw=\n-----END PRIVATE KEY-----\n",
            "client_email": "pdf-extractor@gen-lang-client-0224447803.iam.gserviceaccount.com",
            "client_id": "101936576530126066428",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pdf-extractor%40gen-lang-client-0224447803.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        with open('credentials.json', 'w') as f:
            json.dump(credentials, f)
        return 'credentials.json'
    except Exception as e:
        st.error(f"Failed to save credentials: {str(e)}")
        return None

def main():
    load_css()
    st.markdown('<h1 class="main-title">PDF Bibliography Extractor</h1>', unsafe_allow_html=True)
    
    try:
        credentials_path = save_credentials()
        if not credentials_path:
            st.error("Failed to initialize Google Sheets credentials")
            return
            
        sheets_client = init_sheets_client(credentials_path)
        
        with st.sidebar:
            st.header("Settings")
            create_new_sheet = st.checkbox("Create new sheet", value=True)
            use_batch_mode = st.checkbox("Use batch mode", value=True, 
                                       help="Process all files at once for faster upload")
            include_abstract = st.checkbox("Include abstract", value=True)
            max_files = st.slider("Maximum files to process", 1, 10, 2)
        
        spreadsheet_id = st.text_input("Enter Google Sheets ID", 
                                     help="You can find this in your Google Sheets URL")
        
        if spreadsheet_id and not validate_spreadsheet_id(spreadsheet_id):
            st.error("Invalid Google Sheets ID format")
            return
            
        uploaded_files = st.file_uploader("Upload PDF files", 
                                        type="pdf", 
                                        accept_multiple_files=True,
                                        help=f"Maximum {max_files} files allowed")
        
        if uploaded_files and spreadsheet_id:
            if len(uploaded_files) > max_files:
                st.markdown(f'<div class="error-message">Please upload maximum {max_files} files at a time</div>', 
                          unsafe_allow_html=True)
                return
                
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            extracted_data = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                with st.spinner(f'Processing {uploaded_file.name}...'):
                    try:
                        pdf_info = extract_pdf_info(uploaded_file)
                        
                        if pdf_info:
                            if not include_abstract:
                                pdf_info.pop('abstract', None)
                                
                            if use_batch_mode:
                                extracted_data.append(pdf_info)
                                st.markdown(
                                    f'<div class="success-message">Successfully processed {uploaded_file.name}</div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                if export_to_sheet(sheets_client, spreadsheet_id, pdf_info, create_new=create_new_sheet):
                                    st.markdown(
                                        f'<div class="success-message">Successfully exported {uploaded_file.name} to Google Sheets</div>',
                                        unsafe_allow_html=True
                                    )
                                else:
                                    st.markdown(
                                        f'<div class="error-message">Failed to export {uploaded_file.name} to Google Sheets</div>',
                                        unsafe_allow_html=True
                                    )
                            st.json(pdf_info)
                        else:
                            st.markdown(
                                f'<div class="error-message">Failed to extract information from {uploaded_file.name}</div>',
                                unsafe_allow_html=True
                            )
                            
                    except Exception as e:
                        st.markdown(
                            f'<div class="error-message">Error processing {uploaded_file.name}: {str(e)}</div>',
                            unsafe_allow_html=True
                        )
                        
                    finally:
                        progress_bar.progress((idx + 1) / total_files)
            
            if use_batch_mode and extracted_data:
                with st.spinner('Uploading to Google Sheets...'):
                    if batch_export(sheets_client, spreadsheet_id, extracted_data):
                        st.markdown(
                            '<div class="success-message">Successfully uploaded all data to Google Sheets</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="error-message">Failed to upload data to Google Sheets</div>',
                            unsafe_allow_html=True
                        )
                        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        
    finally:
        if os.path.exists('credentials.json'):
            os.remove('credentials.json')

if __name__ == "__main__":
    main()
