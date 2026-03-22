import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import io

# Constants
GOOGLE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1WR6PAJb3NVX0ynq-_SRJKhFWXQcrkXDKwGdioG-1Ilw/export?format=csv"
)
SCRAPING_URL_TEMPLATE = "https://www.nexperia.com/chemical-content/{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
OUTPUT_FILE = (
    "/root/projects/portfolio_projects/assent_ke_projects/nexperia/reach_svhc_data.xlsx"
)

# ----------------------------------------
# Asynchronous function to fetch REACH SVHC data for a given part number
# ----------------------------------------
async def fetch_reach_data(session, part_number):
    url = SCRAPING_URL_TEMPLATE.format(part_number)
    try:
        async with session.get(url, headers=HEADERS) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, 'html.parser')

            # Scan all <td> elements for specific keyword indicating SVHC data
            td_elements = soup.find_all('td')
            for td in td_elements:
                if "REACH SVHC substance" in td.get_text():
                    text = td.get_text()

                    # Extract CAS number using regex (format: xxx-xx-x)
                    cas_match = re.search(r"substance (\d{3,}-\d{2,}-\d{1,})", text)
                    cas_no = cas_match.group(1) if cas_match else None

                    # Extract PPM (parts per million) amount from text
                    ppm_match = re.search(r"at (\d+) ppm", text)
                    ppm_amount = ppm_match.group(1) if ppm_match else None

                    return part_number, part_number, cas_no, ppm_amount

            # If no SVHC substance found, return part number with None values
            return part_number, part_number, None, None
    except Exception as e:
        print(f"🚨 Error fetching data for part number: {part_number}, Error: {e}")
        return part_number, part_number, None, None

# ----------------------------------------
# Function to process multiple part numbers concurrently using asyncio
# ----------------------------------------
async def process_part_numbers(part_numbers):
    async with aiohttp.ClientSession() as session:
        # Create asynchronous tasks for each part number
        tasks = [fetch_reach_data(session, part_number) for part_number in part_numbers]
        results = await asyncio.gather(*tasks)
    return results

# ----------------------------------------
# Main driver function
# ----------------------------------------
def main():
    try:
        # Step 1: Download part numbers from the provided Google Sheet CSV
        response = requests.get(GOOGLE_SHEET_URL)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        # Extract list of part numbers from the 'successful_pn' column
        part_numbers = df['successful_pn'].dropna().tolist()

        # Step 2: Perform asynchronous web scraping
        print("🔄 Starting asynchronous scraping...")
        results = asyncio.run(process_part_numbers(part_numbers))

        # Step 3: Save the extracted data to an Excel file
        output_df = pd.DataFrame(results, columns=[
            'Original Part Number (successful_pn)',
            'Processed Part Number', 
            'REACH SVHC Substance CAS No.', 
            'PPM Amount'
        ])
        output_df.to_excel(OUTPUT_FILE, index=False)
        print(f"✅ Data saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"🚨 An error occurred: {e}")

# ----------------------------------------
# Entry point for script execution
# ----------------------------------------
if __name__ == "__main__":
    main()
