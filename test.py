import json

url_list = list()
with open("url.json", "r") as file:
    url_list.extend(json.loads(file.read()))
print(url_list)
