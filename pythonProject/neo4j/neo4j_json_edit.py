import json


def json_save(data, file_path):
    with open('neo4j_data.json', 'w') as file:
        json.dump(data, file)


def json_load(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data






