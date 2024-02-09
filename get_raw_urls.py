import json
from typing import Dict, List
import os

def get_raw_urls(orig_urls_file: str) -> None:
    orig_urls = []
    raw_urls = []
    
    with open(orig_urls_file, 'r') as f:
        data = json.load(f)
        orig_urls = data["orig_urls"]
    
    for orig_url in orig_urls:
        raw_url = orig_url.replace("github.com", "raw.githubusercontent.com").replace("blob/", "")
        id_index = raw_url.rfind("#")
        id_index = len(raw_url) if id_index == -1 else id_index

        raw_urls.append(raw_url[:id_index])

    output_data = {"raw_urls": raw_urls}
    with open("code_search/raw_data_all.json", 'w') as f:
        json.dump(output_data, f, indent = 4)

if __name__ == "__main__":
    get_raw_urls("code_search/data_all.json")