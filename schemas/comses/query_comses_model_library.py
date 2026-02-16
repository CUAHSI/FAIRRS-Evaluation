import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin

# --- Configuration ---
BASE_URL = "https://www.comses.net"
START_URL = "https://www.comses.net/codebases/"
OUTPUT_DIR = "codemeta"
HEADERS = {
    "User-Agent": "Metadata-Research-Bot/1.0 (Contact: your_email@example.com)"
}

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_codebase_links(page_url):
    """Scrapes the search/list page for links to individual models."""
    print(f"Scanning list page: {page_url}")
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Collect links to models
        links = set()
        for a in soup.find_all("a", href=True):
            href = a['href']
            # Pattern: /codebases/[UUID]/
            if href.startswith("/codebases/") and len(href.strip("/").split("/")) >= 2:
                links.add(urljoin(BASE_URL, href))
        
        # Check for 'Next' page in pagination
        next_page = None
        next_btn = soup.find("a", string=lambda t: t and "Next" in t)
        if next_btn:
            next_page = urljoin(BASE_URL, next_btn['href'])
            
        return list(links), next_page
    except Exception as e:
        print(f"Error scanning {page_url}: {e}")
        return [], None

def extract_codemeta_from_html(model_url):
    """Visits model page and extracts JSON-LD from the <script> tag."""
    try:
        print(f"  Fetching: {model_url}")
        response = requests.get(model_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Locate the specific JSON-LD script tag
        script_tag = soup.find("script", type="application/ld+json")
        
        if script_tag and script_tag.string:
            # Parse the text as JSON to ensure it's valid
            metadata = json.loads(script_tag.string)
            
            # Use the model UUID as the filename
            # e.g., /codebases/15a2fc42-90bd-42c4-b21b-dfba428cdb16/...
            model_id = model_url.split("/codebases/")[1].split("/")[0]
            
            save_path = os.path.join(OUTPUT_DIR, f"{model_id}.json")
            with open(save_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=4)
                
            print(f"    [OK] Saved metadata to {save_path}")
        else:
            print(f"    [!] No JSON-LD found on page.")

    except Exception as e:
        print(f"    [!] Error processing {model_url}: {e}")

def main():
    ensure_dir(OUTPUT_DIR)
    current_url = START_URL
    # page_limit = 3  # Increase or remove this for a full scrape
    current_page = 1

    while current_url:
        print(f"\n--- Processing Page {current_page} ---")
        links, next_url = get_codebase_links(current_url)
        
        for link in links:
            extract_codemeta_from_html(link)
            time.sleep(1) # Politeness delay
            
        current_url = next_url
        current_page += 1
        time.sleep(2)

    print("\nExtraction complete.")

if __name__ == "__main__":
    main()