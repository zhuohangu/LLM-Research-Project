import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
import time

file_name = "completion_500"
per_page = 100
pages = 5
token = "token"

url_list = [
	f"https://api.github.com/search/code?q=openai.ChatCompletion.create&ref=advsearch&per_page={per_page}&page="
]
accept = "application/vnd.github+json"
authorization = "Bearer " + token
x_GitHub_Api_Version = "2022-11-28"
headers = {"Accept": accept, "Authorization": authorization, "X-GitHub-Api-Version": x_GitHub_Api_Version}
payload = {"Authorization": "Bearer " + token}

repo_dict = {}
id_list = []
with requests.session() as s:
    for url in url_list:
        for page in range(1, pages + 1):
            while True:  # Sleep the timeout
                res = s.get(url + str(page), headers = headers)
                
                if res.status_code != 200:
                    print("--------- break at", page, "---", res.status_code)
                    time.sleep(5)
                    continue
                else:
                	print("--------- good at", page, "---", res.status_code)
                	break
            
            res_json = json.loads(str(res.content, 'utf-8'))
            res_items = res_json['items']
            
            for repo in res_items:
                score = repo.get("score")
                repo_name = repo.get("name")
                repo_id = repo.get("repository").get("id")
                repo_url = repo.get("repository").get("html_url")
                repo_file_url = repo.get("html_url")
                if repo_id not in id_list:
                    repo_dict[repo_id] = {"score": score,
                                            "name": repo_name,
                                            "url": repo_url,
                                            "file_url": repo_file_url}
                    id_list.append(repo_id)
#                 else:
#                     print("Duplicated:", repo_name)

print(f"Number of Repos (out of {pages * per_page}):", len(list(repo_dict.keys())))
dump_path = open(f"code_search/{file_name}.json", "w")
json.dump(repo_dict, dump_path, indent = 4)
dump_path.close()

