import json

def load_config(json_path):
    data = ''
    with open(json_path, 'r') as f:
        data = f.read()
    data = data.replace('\n', '')
    return json.loads(data)