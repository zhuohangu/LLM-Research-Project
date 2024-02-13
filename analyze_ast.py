import ast  # Documentation: https://docs.python.org/3/library/ast.html
import json
import os
from urllib.request import urlopen
from typing import Dict, List

def parse_py_files_from_json(json_file):
    with open(json_file, 'r') as file:
        urls = json.load(file)
    py_urls = [url for url in urls["raw_urls"] if ".py" in url]  # Adjusted to include URLs containing ".py"
    return py_urls

def get_create_calls(tree: ast.Module) -> List[Dict[str, any]]:
    calls = []
    for statement in ast.walk(tree):
        if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Attribute) and statement.func.attr == 'create':
            messages_arg = next((kw for kw in statement.keywords if kw.arg == "messages"), None)
            if messages_arg:
                calls.append({
                    "func": ast.unparse(statement.func.value),
                    "messages": ast.unparse(messages_arg.value)
                })
    return calls

def extract_f_strings(tree: ast.Module) -> List[str]:
    f_strings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            f_string = ast.unparse(node)
            f_strings.append(f_string)
        elif isinstance(node, ast.Call) and hasattr(node.func, 'id') and node.func.id == 'format':
            base_str = ast.unparse(node.func.value)
            if "{" in base_str and "}" in base_str:  # rudimentary check for dynamic parts
                f_strings.append(base_str)
    return f_strings

def process_python_file(url):
    try:
        # Assuming you have a way to download/read Python files from URLs
        response = urlopen(url)
        content = response.read().decode('utf-8')
        tree = ast.parse(content)
        
        create_calls = get_create_calls(tree)
        f_strings = extract_f_strings(tree)
        return create_calls, f_strings

    except Exception as e:
        print(f"Error downloading or parsing {url}: {e}")
    return [], []


def save_results_to_json(results, file_path):
    with open(file_path, 'w') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    # Main processing logic
    py_urls = parse_py_files_from_json('code_search/raw_data_all.json')
    # py_urls = ["https://raw.githubusercontent.com/MLNLP-World/AI-Paper-Collector/477ef2aec293e07156f386d7dccd27fa2c1af295/app.py"]
    results = []
    
    for url in py_urls:
        create_calls, f_strings = process_python_file(url)
        results.append({
            "url": url,
            "create_calls": create_calls,
            "f_strings": f_strings
        })

    # Specify the desired output JSON file name
    output_file_name = 'code_search/found_patterns_data_all.json'
    save_results_to_json(results, output_file_name)
