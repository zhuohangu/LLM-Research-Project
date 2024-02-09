import openai
import json
import interpreter
import os

with open('tokens.json') as f:
    d = json.load(f)
    os.environ['OPENAI_API_KEY'] = d["OPENAI_API_KEY"] 

url_test = 'https://raw.githubusercontent.com/assafelovic/gpt-researcher/b40e5c6ad2e58858dc7d4c21f9db7df64c6c4311/permchain_example/editor_actors/editor.py'

message = f'Tell me the template in the code. Are there any dynamic tokens in this template? {url_test}'
interpreter.chat(message)
interpreter.reset()
