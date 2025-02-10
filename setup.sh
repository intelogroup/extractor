#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install streamlit==1.32.0
pip install PyPDF2==3.0.1
pip install gspread==6.0.2
pip install google-auth==2.28.1
pip install google-auth-oauthlib==1.2.0
pip install pyyaml==6.0.1
