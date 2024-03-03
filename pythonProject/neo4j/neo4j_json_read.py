import json

with open('neo4j_data.json', 'r') as file:
    neo4j_data = json.load(file)

URI = neo4j_data['URL']
AUTH = (neo4j_data['AUTH_id'], neo4j_data["AUTH_password"])







