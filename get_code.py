import json
import os
from urllib.request import urlopen

from utils import Path

def retrieve_code(in_path: str, in_file: str, out_path: str) -> None:
    with open(os.path.join(in_path, in_file), 'r') as f:
        data = json.load(f)
        url_list = data["raw_urls"]
    
    for (i, url) in enumerate(url_list):
        with open(os.path.join(out_path, f"tmp{i}.py"), 'w+') as f:
            f.write(
                urlopen(url).read().decode("utf-8")
            )
    
retrieve_code(
    'code_search', 
    'completion_500.json', 
    os.path.join(Path.TRACE_DIR, "holdout")
)