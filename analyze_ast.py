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




# def load_urls(json_file):
#     with open(json_file, 'r') as f:
#         data = json.load(f)
#     return data.get("raw_urls", [])

# def download_and_parse(url):
#     try:
#         response = urlopen(url)
#         content = response.read().decode('utf-8')
#         if url.endswith('.py'):  # Check if it's likely a Python file
#             return ast.parse(content)
#     except Exception as e:
#         print(f"Error downloading or parsing {url}: {e}")
#     return None

# def search_ast(tree):
#     patterns_found = {
#         "openai_chat_completion_calls": [],
#         "f_string_assignments": []
#     }

#     for node in ast.walk(tree):
#         # Check for ChatCompletion.create calls
#         if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and \
#            node.func.attr == 'create' and \
#            isinstance(node.func.value, ast.Attribute) and node.func.value.attr == 'ChatCompletion' and \
#            isinstance(node.func.value.value, ast.Name) and node.func.value.value.id == 'openai':
#             call_snippet = ast.unparse(node.func.value) + '.' + ast.unparse(node.func) + '('
#             patterns_found["openai_chat_completion_calls"].append(call_snippet)
        
#         # Check for assignments of f-strings
#         elif isinstance(node, ast.Assign):
#             for target in node.targets:
#                 if isinstance(node.value, ast.JoinedStr):
#                     f_string = ast.unparse(node.value)
#                     variable = ast.unparse(target)
#                     patterns_found["f_string_assignments"].append({"variable": variable, "f_string": f_string})

#     return patterns_found

# def process_urls_and_save(urls, output_file):
#     results = []

#     for url in urls:
#         tree = download_and_parse(url)
#         if tree:
#             found_patterns = search_ast(tree)
#             if found_patterns["openai_chat_completion_calls"] or found_patterns["f_string_assignments"]:
#                 results.append({"url": url, "patterns": found_patterns})

#     with open(output_file, 'w') as f:
#         json.dump(results, f, indent=4)


# if __name__ == "__main__":
#     raw_urls_file = "code_search/raw_urls_file_500.json"
#     output_file = "code_search/found_patterns_2.json"
#     urls = load_urls(raw_urls_file)
#     process_urls_and_save(urls, output_file)



# with open("code_search/test.py", 'r') as f:
#     tree = ast.parse(f.read())

# with open("code_search/ast.txt", 'w') as f:
#     f.write(str(
#         ast.dump(tree, indent = 4)
#     ))
    
# with open(os.path.join('code_search', 'test.py'), 'w+') as f:
#     f.write(
#             urlopen(url_test).read().decode("utf-8")
#             )

# def create_calls(tree):
#     for statement in ast.walk(tree):
#         if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Attribute) and\
#               statement.func.attr == 'create':
#             yield {
#                 'model': ast.unparse(statement.func.value),
#                 'args': [ast.unparse(j) for j in statement.args],
#                 'kwargs': {j.arg: ast.unparse(j.value) for j in statement.keywords}
#             }

# def prompt_trace(tree):
#     for statement in ast.walk(tree):
#         if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str):
#             yield {
#                     'variable': [ast.unparse(target) for target in statement.targets],
#                     'string': statement.value.value
#                 }

# print(list(create_calls(tree)))
# print(list(prompt_trace(tree)))


# for statement in ast.walk(tree):
#     if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Attribute):
#         if statement.func.attr == 'create' and isinstance(statement.func.value, ast.Attribute):
#             if statement.func.value.attr == 'ChatCompletion':
#                 pass