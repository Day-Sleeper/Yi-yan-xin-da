import json


def json_save(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def json_load(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data






