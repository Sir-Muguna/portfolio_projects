import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
from bs4 import BeautifulSoup
import gdown
from concurrent.futures import ThreadPoolExecutor

def get_retry_session():
    session = requests.Session()
    retries = Retry(
        total=5, 
        backoff_factor=0.5, 
        status_forcelist=[500, 502, 503, 504], 
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def process_part(part, session):
    print(f"Checking: {part}")
    search_url = f"https://www.kemet.com/en/us/search.html?q={part}"
    try:
        response = session.get(search_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve page for {part}. Status code: {response.status_code}")
            return {'part_number': part, 'Found': False, 'Download Link': None}
    except Exception as e:
        print(f"Request failed for {part}: {e}")
        return {'part_number': part, 'Found': False, 'Download Link': None}

    soup = BeautifulSoup(response.text, "html.parser")
    match = soup.find("a", href=re.compile(r"/component-documentation/download/specsheet/"))
    if match:
        href = match['href']
        full_link = f"https://search.kemet.com{href}" if href.startswith('/') else href
        return {'part_number': part, 'Found': True, 'Download Link': full_link}
    else:
        return {'part_number': part, 'Found': False, 'Download Link': None}

def main():
    file_id = "1lvn4xrIHC2AYF7wHCNlBWPLJe30nH2N3qD6SimAJPg8"
    sheet_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    try:
        # Download the file using gdown
        excel_file = "downloaded_sheet.xlsx"
        gdown.download(sheet_url, excel_file, quiet=False)
        
        # Load the Excel file into pandas
        df = pd.read_excel(excel_file)
    except Exception as e:
        raise ValueError(f"Error loading Google Sheet: {e}")

    if 'part_number' not in df.columns:
        raise ValueError("Google Sheet must have a column named 'part_number'")

    session = get_retry_session()

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda part: process_part(part, session), df['part_number']))

    output_df = pd.DataFrame(results)
    output_filename = "kemet_search_summary.xlsx"
    try:
        output_df.to_excel(output_filename, index=False)
        print(f"Results successfully saved to {output_filename}")
    except Exception as e:
        print(f"Error saving results to Excel: {e}")

if __name__ == "__main__":
    main()
