# /// script
# dependencies = [
#   "requests",
# ]
# ///

import requests
import os
import time

class Photostream:
    def __init__(self, immich_api_key: str, immich_server: str):
        self.api_key = immich_api_key
        self.base_url = f"https://{immich_server}/api"
        self.image_dir = "Photostream"

    def get_buckets(self):
        url = f"{self.base_url}/timeline/buckets?size=DAY"
        response = requests.get(url, headers={"x-api-key": self.api_key})
        return response.json()[:7] # a week

    def list_assets_for_bucket(self, bucket: dict):
        url = f"{self.base_url}/timeline/bucket?size=DAY&timeBucket={bucket['timeBucket']}&withExif=true"
        response = requests.get(url, headers={"x-api-key": self.api_key})
        return response.json()
    
    def download_asset(self, asset: dict):
        url = f"{self.base_url}/assets/{asset['id']}/original"
        response = requests.get(url, headers={"x-api-key": self.api_key, "accept": "octet-stream"})
        with open(f"{self.image_dir}/" + asset['originalFileName'], "wb") as f:
            f.write(response.content)
            
    def clear_old_assets(self):
        for file in os.listdir(self.image_dir):
            file_path = os.path.join(self.image_dir, file)
            file_age_in_seconds = os.path.getmtime(file_path)
            file_age_in_days = (time.time() - file_age_in_seconds) / (60 * 60 * 24)
            if file_age_in_days > 30:
                os.remove(file_path)
    
    def main(self):
        self.clear_old_assets() # Clear old assets
        buckets = self.get_buckets() # Get bucket for last week
        
        # Get all assets from each bucket
        assets = []
        for bucket in buckets:
            assets.extend(self.list_assets_for_bucket(bucket)) 
            
        print(f"Found {len(assets)} assets")
        
        assets = reversed(assets) # Download the assets in reverse order
        # Download the assets        
        for asset in assets:
            if os.path.exists(f"{self.image_dir}/{asset['originalFileName']}"):
                print(f"Skipping {asset['originalFileName']} because it already exists")
                continue
            else:
                self.download_asset(asset)

if __name__ == "__main__":
    photostream = Photostream(immich_api_key=os.getenv("IMMICH_API_KEY"), immich_server=os.getenv("IMMICH_SERVER"))
    photostream.main()