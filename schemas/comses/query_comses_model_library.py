import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
from urllib.parse import urljoin

# --- Configuration ---
BASE_URL = "https://www.comses.net"
SEARCH_BASE_URL = "https://www.comses.net/codebases/?page="
OUTPUT_DIR = "schemas/comses/codemeta"
HEADERS = {
    "User-Agent": "Metadata-Research-Bot/1.0 (Contact: your_email@example.com)"
}

# Regex to match exactly /codebases/{uuid}/
MODEL_URL_PATTERN = re.compile(r"^/codebases/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/?$")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_model_links_from_page(page_num):
    """Scrapes a specific page number for links to individual models using strict Regex."""
    page_url = f"{SEARCH_BASE_URL}{page_num}"
    print(f"Scanning list page: {page_url}")
    
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        if response.status_code == 404:
            return set()
            
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        links = set()
        for a in soup.find_all("a", href=True):
            href = a['href']
            if MODEL_URL_PATTERN.match(href):
                links.add(urljoin(BASE_URL, href))
        return links
    except Exception as e:
        print(f"Error scanning page {page_num}: {e}")
        return set()

def extract_codemeta_from_html(model_url):
    """Checks for local file existence, then fetches and saves JSON-LD if missing."""
    try:
        # 1. Extract the ID from the URL
        parts = model_url.rstrip("/").split("/")
        model_id = parts[-1]
        
        # 2. Check if the file already exists locally
        save_path = os.path.join(OUTPUT_DIR, f"{model_id}.json")
        if os.path.exists(save_path):
            print(f"  [Skip] {model_id}.json already exists locally.")
            return

        # 3. Only fetch if the file is missing
        print(f"  Fetching Model: {model_id}")
        response = requests.get(model_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")
        
        if script_tag and script_tag.string:
            metadata = json.loads(script_tag.string)
            with open(save_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=4)
            print(f"    [OK] Saved")
        else:
            print(f"    [!] No JSON-LD found.")

    except Exception as e:
        print(f"    [!] Error processing {model_url}: {e}")

def main():
    ensure_dir(OUTPUT_DIR)
    
    current_page = 1
    MAX_PAGES = 5 

    while current_page <= MAX_PAGES:
        print(f"\n--- Processing Page {current_page} ---")
        links = get_model_links_from_page(current_page)
        
        if not links:
            print("No models found on this page. Stopping extraction.")
            break
            
        print(f"  -> Found {len(links)} valid model links.")
        
        for link in links:
            extract_codemeta_from_html(link)
            # Politeness delay only if we are actually making a request
            # We'll keep it short since we're only hitting model pages now
            time.sleep(0.5) 
            
        current_page += 1
        time.sleep(1) 

    print("\nExtraction complete.")

if __name__ == "__main__":
    main()