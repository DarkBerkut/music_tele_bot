import csv
import json
import requests

input_str = input()


def file_to_dict(file):
    return {row[1].lower(): row[0] for row in csv.reader(open(file))}

categories = [i.strip() for i in input_str.split(',')]
indxs = []

for category in categories:
    for file in ['data/style.csv', 'data/theme.csv', 'data/time.csv', 'data/language.csv', 'data/tempo.csv']:
        categ_dict = file_to_dict(file)
        ind = categ_dict.get(category.lower())
        if ind:
            indxs.append(ind)

values = ','.join(['{}:10'.format(i) for i in indxs])
data = {'values': values, 'size': 20, 'operator': 'AND'}

r = requests.post("http://muzis.ru/api/stream_from_values.api", data=data)

songs = json.loads(r.text)['songs']

result = []
for song in songs:
    result.append(song['id'])

result = ' '.join([str(i) for i in result])
print(result)
