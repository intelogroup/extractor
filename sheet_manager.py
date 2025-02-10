import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict

def init_sheets_client(credentials_path: str) -> gspread.Client:
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials = Credentials.from_service_account_file(
        credentials_path, 
        scopes=scope
    )
    return gspread.authorize(credentials)

def setup_sheet(sheet) -> None:
    """Setup sheet with headers and formatting"""
    headers = ['Title', 'Authors', 'Year', 'Journal', 'DOI', 'Abstract', 'Timestamp']
    sheet.clear()
    sheet.append_row(headers)
    
    # Format header row
    header_format = {
        'textFormat': {'bold': True},
        'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}
    }
    sheet.format('A1:G1', header_format)
    
    # Adjust column widths
    sheet.columns_auto_resize(0, 7)

def export_to_sheet(client: gspread.Client, spreadsheet_id: str, data: Dict[str, str], create_new: bool = False) -> bool:
    try:
        workbook = client.open_by_key(spreadsheet_id)
        sheet = workbook.sheet1
        
        if create_new or sheet.row_count <= 1:
            setup_sheet(sheet)
        
        # Prepare row data
        from datetime import datetime
        row = [
            data.get('title', ''),
            data.get('authors', ''),
            data.get('year', ''),
            data.get('journal', ''),
            data.get('doi', ''),
            data.get('abstract', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
        
        sheet.append_row(row)
        return True
        
    except Exception as e:
        print(f"Error exporting to sheet: {e}")
        return False

def batch_export(client: gspread.Client, spreadsheet_id: str, data_list: List[Dict[str, str]]) -> bool:
    try:
        workbook = client.open_by_key(spreadsheet_id)
        sheet = workbook.sheet1
        
        if sheet.row_count <= 1:
            setup_sheet(sheet)
            
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        rows = [[
            data.get('title', ''),
            data.get('authors', ''),
            data.get('year', ''),
            data.get('journal', ''),
            data.get('doi', ''),
            data.get('abstract', ''),
            timestamp
        ] for data in data_list]
        
        sheet.append_rows(rows)
        return True
        
    except Exception as e:
        print(f"Error in batch export: {e}")
        return False
