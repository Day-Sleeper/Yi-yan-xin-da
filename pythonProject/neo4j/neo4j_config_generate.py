import json
neo4j_data = {
    "URL": "bolt://localhost:7687",
    "AUTH_id": "user123",
    "AUTH_password": "ai123hr456"
}

# 将数据转换为JSON格式
json_data = json.dumps(neo4j_data, indent=4)

# 将JSON数据写入文件
with open('neo4j_data.json', 'w') as file:
    file.write(json_data)
