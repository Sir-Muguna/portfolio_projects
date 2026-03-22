# api_requester.py
import requests
import pandas as pd
import json
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_requests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AmazonDataRequester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Amazon-Data-ETL/1.0',
            'Accept': 'application/json'
        })
    
    def health_check(self):
        """Check if API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ API is healthy")
                return True
            else:
                logger.warning(f"API returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API health check failed: {e}")
            return False
    
    def check_master_sheet_exists(self):
        """Check if master sheet has been generated"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/master-sheet?page=1&per_page=1",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data['total'] > 0
            elif response.status_code == 404:
                return False
            else:
                logger.warning(f"Unexpected response: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking master sheet: {e}")
            return False
    
    def generate_master_sheet(self, entries=2500):
        """Generate master sheet data"""
        try:
            logger.info(f"Generating master sheet with {entries} entries...")
            response = self.session.post(
                f"{self.base_url}/api/generate-master?entries={entries}",
                timeout=60  # Longer timeout for master generation
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Master sheet generated: {data['message']}")
                logger.info(f"Total entries: {data['count']}")
                return True
            else:
                logger.error(f"❌ Failed to generate master sheet: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error generating master sheet: {e}")
            return False
    
    def generate_daily_data(self, entries=100):
        """Generate daily data"""
        try:
            logger.info(f"Generating {entries} daily entries...")
            response = self.session.post(
                f"{self.base_url}/api/daily-data?entries={entries}",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Daily data generated: {data['message']}")
                logger.info(f"Total entries: {data['count']}")
                return True
            else:
                logger.error(f"❌ Failed to generate daily data: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error generating daily data: {e}")
            return False
    
    def fetch_daily_data(self, max_pages=None):
        """Fetch all daily data with pagination"""
        try:
            all_data = []
            page = 1
            per_page = 100
            
            logger.info("Fetching daily data...")
            
            while True:
                if max_pages and page > max_pages:
                    break
                    
                logger.info(f"Fetching page {page}...")
                response = self.session.get(
                    f"{self.base_url}/api/daily-data?page={page}&per_page={per_page}",
                    timeout=15
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to fetch page {page}: {response.text}")
                    break
                
                data = response.json()
                all_data.extend(data['data'])
                
                logger.info(f"Page {page}: {len(data['data'])} records")
                
                # Check if we've reached the last page
                if len(data['data']) < per_page:
                    break
                    
                page += 1
                time.sleep(0.1)  # Small delay to be polite to the server
            
            logger.info(f"✅ Total records fetched: {len(all_data)}")
            return pd.DataFrame(all_data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching daily data: {e}")
            return pd.DataFrame()
    
    def fetch_master_data(self, max_pages=None):
        """Fetch master sheet data with pagination"""
        try:
            all_data = []
            page = 1
            per_page = 100
            
            logger.info("Fetching master sheet data...")
            
            while True:
                if max_pages and page > max_pages:
                    break
                    
                logger.info(f"Fetching master page {page}...")
                response = self.session.get(
                    f"{self.base_url}/api/master-sheet?page={page}&per_page={per_page}",
                    timeout=15
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to fetch master page {page}: {response.text}")
                    break
                
                data = response.json()
                all_data.extend(data['data'])
                
                logger.info(f"Master Page {page}: {len(data['data'])} records")
                
                # Check if we've reached the last page
                if len(data['data']) < per_page:
                    break
                    
                page += 1
                time.sleep(0.1)
            
            logger.info(f"✅ Total master records fetched: {len(all_data)}")
            return pd.DataFrame(all_data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching master data: {e}")
            return pd.DataFrame()
    
    def save_data(self, df, filename_prefix="amazon_data"):
        """Save data to file with timestamp"""
        if df.empty:
            logger.warning("No data to save")
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.parquet"
            
            df.to_parquet(filename, index=False)
            logger.info(f"✅ Data saved to {filename}")
            logger.info(f"File size: {len(df)} records")
            
            # Also save a sample as JSON for inspection
            sample_filename = f"{filename_prefix}_sample_{timestamp}.json"
            sample_data = df.head(10).to_dict('records')
            with open(sample_filename, 'w') as f:
                json.dump(sample_data, f, indent=2, default=str)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving data: {e}")
            return False
    
    def run_full_etl(self, generate_master_if_missing=True):
        """Run complete ETL process"""
        logger.info("🚀 Starting Amazon Data ETL Process")
        logger.info("=" * 50)
        
        # Step 1: Health check
        if not self.health_check():
            logger.error("ETL process aborted - API not available")
            return False
        
        # Step 2: Check if master sheet exists
        logger.info("Checking if master sheet exists...")
        master_exists = self.check_master_sheet_exists()
        
        if not master_exists:
            if generate_master_if_missing:
                logger.info("Master sheet not found, generating now...")
                if not self.generate_master_sheet(2500):
                    logger.error("Failed to generate master sheet, aborting ETL")
                    return False
                # Wait a moment for the master sheet to be fully generated
                time.sleep(2)
            else:
                logger.error("Master sheet not found and generation disabled, aborting ETL")
                return False
        else:
            logger.info("✅ Master sheet already exists")
        
        # Step 3: Generate daily data
        if not self.generate_daily_data(entries=100):
            logger.warning("Failed to generate daily data, trying to fetch existing data")
        
        # Step 4: Fetch daily data
        daily_df = self.fetch_daily_data()
        if not daily_df.empty:
            self.save_data(daily_df, "daily_amazon_data")
            
            # Show some statistics
            logger.info("\n📊 Daily Data Statistics:")
            logger.info(f"Total records: {len(daily_df)}")
            if 'net_profit' in daily_df.columns:
                logger.info(f"Total profit: ${daily_df['net_profit'].sum():.2f}")
                logger.info(f"Profitable items: {(daily_df['net_profit'] > 0).sum()}")
            if 'status' in daily_df.columns:
                status_counts = daily_df['status'].value_counts()
                for status, count in status_counts.items():
                    logger.info(f"Status '{status}': {count} items")
        else:
            logger.warning("No daily data available")
        
        # Step 5: Optional - Fetch master data
        master_df = self.fetch_master_data(max_pages=2)  # Just first 2 pages for demo
        if not master_df.empty:
            self.save_data(master_df, "master_amazon_data")
        else:
            logger.warning("No master data available")
        
        logger.info("✅ ETL process completed successfully")
        return True

def main():
    """Main function to run the API requests"""
    # Initialize the requester
    requester = AmazonDataRequester()
    
    # Run the full ETL process (will generate master sheet if missing)
    success = requester.run_full_etl(generate_master_if_missing=True)
    
    if success:
        print("\n🎉 ETL process completed successfully!")
        print("Check the log file 'api_requests.log' for details")
    else:
        print("\n❌ ETL process failed!")
        print("Check the log file 'api_requests.log' for error details")

if __name__ == "__main__":
    main()