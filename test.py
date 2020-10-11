import json

l = list()
with open('movie_detail.json', 'r') as file:
    text_lines = file.readlines()
    for line in text_lines:
        l.append(json.loads(line))
with open('movie_detail.json', 'w+') as f:
    f.write(json.dumps(l, ensure_ascii=False))
