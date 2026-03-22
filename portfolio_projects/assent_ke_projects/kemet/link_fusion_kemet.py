import os
import re
import pandas as pd
import gdown
import pdfplumber
from PyPDF2 import PdfMerger
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
DOWNLOAD_DIR = "raw_downloads"
MERGED_DIR = "merged_pdfs"
SUMMARY_PATH = "termination_summary.xlsx"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1vjYbwf2Wcru0IjsgqtZc3ZFr1n-u4b6y/export?format=csv"  # Export as CSV

# Setup directories
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(MERGED_DIR, exist_ok=True)

def load_sheet_to_dataframe(sheet_url):
    """Load Google Sheet data directly into a DataFrame."""
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [c.strip().lower() for c in df.columns]
        df.fillna("", inplace=True)  # Replace NaN with empty strings
        print("✅ Google Sheet loaded successfully.")
        print("🔍 Columns:", df.columns.tolist())
        return df
    except Exception as e:
        raise ValueError(f"Error loading Google Sheet: {e}")

def validate_columns(df, required_columns):
    """Validate that required columns exist in the DataFrame."""
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns: {required_columns - set(df.columns)}")

def detect_file_type(file_path):
    """Detect the type of a file based on its content."""
    with open(file_path, 'rb') as f:
        sig = f.read(8)
        if sig.startswith(b'%PDF'):
            return '.pdf'
    return None

def extract_termination_type(pdf_path):
    """Extract the termination type from the first page of a PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text() or ""
            match = re.search(r"Termination\s*[:\-]?\s*(.+)", text, re.IGNORECASE)
            if match:
                raw_term = match.group(1).strip().lower()
                if "lead" in raw_term or "snpb" in raw_term:
                    return "Lead"
                elif "tin" in raw_term:
                    return "Tin"
                else:
                    return "Other"
        return "Other"
    except Exception as e:
        print(f"⚠ Error reading {pdf_path}: {e}")
        return "Other"

def process_row(idx, row):
    """Download and process a single row."""
    client = str(row["client"]).strip()
    label = str(row["label"]).strip()
    url = str(row["links"]).strip()

    if not url.lower().startswith(("http://", "https://")):
        print(f"✖ Skipping invalid URL at row {idx}: {url}")
        return None

    client_safe = re.sub(r"\W+", "_", client.lower())
    label_safe = re.sub(r"\W+", "_", label.lower()) if label else "nolabel"
    temp_path = os.path.join(DOWNLOAD_DIR, f"tmp_{idx}.pdf")

    try:
        gdown.download(url, temp_path, quiet=True, fuzzy=True)
    except Exception as e:
        print(f"⚠ Download failed at row {idx}: {e}")
        return None

    if not os.path.exists(temp_path) or detect_file_type(temp_path) != '.pdf':
        print(f"⚠ Invalid or non-PDF file at row {idx}")
        return None

    termination_type = extract_termination_type(temp_path)
    termination_safe = re.sub(r"\W+", "_", termination_type.lower())
    final_path = os.path.join(DOWNLOAD_DIR, f"{client_safe}_{label_safe}_{termination_safe}_{idx}.pdf")
    os.rename(temp_path, final_path)

    print(f"✔ Row {idx}: {termination_type}")
    return {
        "client": client_safe,
        "label": label_safe,
        "termination": termination_type,
        "termination_safe": termination_safe,
        "file_path": final_path,
        "link": url
    }

def merge_pdfs(pdf_groups):
    """Merge PDFs grouped by client, label, and termination type."""
    merged_count = 0
    for (client_safe, label_safe, termination_safe), file_list in pdf_groups.items():
        merged_pdf_path = os.path.join(MERGED_DIR, f"{client_safe}_{label_safe}_{termination_safe}.pdf")
        merger = PdfMerger()
        for file in file_list:
            merger.append(file)
        merger.write(merged_pdf_path)
        merger.close()
        merged_count += 1
        print(f"✅ Merged PDF: {merged_pdf_path}")
    return merged_count

def main():
    df = load_sheet_to_dataframe(GOOGLE_SHEET_URL)
    validate_columns(df, {"client", "label", "links"})

    summary_records = []
    pdf_groups = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_row, idx, row) for idx, row in df.iterrows()]
        for future in as_completed(futures):
            result = future.result()
            if result:
                key = (result["client"], result["label"], result["termination_safe"])
                pdf_groups.setdefault(key, []).append(result["file_path"])
                summary_records.append({"link": result["link"], "termination": result["termination"]})

    merged_count = merge_pdfs(pdf_groups)

    summary_df = pd.DataFrame(summary_records)
    summary_df.to_excel(SUMMARY_PATH, index=False)
    print(f"\n🎉 Done! {merged_count} merged files saved to: {MERGED_DIR}")
    print(f"\n📄 Termination summary saved to: {SUMMARY_PATH}")

if __name__ == "__main__":
    main()
