from neo4j import GraphDatabase, RoutingControl


URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ai123hr456")



def initial_data():
    global main_data
    main_data = {}

def add_friend(driver, name, friend_name):
    driver.execute_query(
        "MERGE (a:Person {name: $name}) "
        "MERGE (friend:Person {name: $friend_name}) "
        "MERGE (a)-[:KNOWS]->(friend)",
        name=name, friend_name=friend_name, database_="neo4j",
    )
def add_point(driver,database_name, point_name, main_label, attribute_name, attribute_value):
    input = "CREATE ({point_name}:{main_label} {{ {attribute_name}: '{attribute_value}' }}) ".format(point_name=point_name, main_label=main_label, attribute_name=attribute_name, attribute_value=attribute_value)
    attribute_data = {}
    attribute_data[attribute_name] = attribute_value
    attribute_data["主标签"] = main_label
    point_data = {}
    point_data[point_name] = attribute_data
    classification__data = {}
    classification__data["点数据"] = point_data
    main_data[database_name] = classification__data
    # driver.execute_query(input,database_="neo4j",)
    return input
#节点必要信息信息：节点名称，主要标签，一个属性（均可以为中文）
def add_relationship(driver, database_name, relationship_start, relationship_end, relationship_label):

    input = "CREATE ({relationship_start})-[:{relationship_label}]->({relationship_end})".format(relationship_start=relationship_start, relationship_end= relationship_end, relationship_label = relationship_label)
    # driver.execute_query(input, database_="neo4j",)
    return input
#关系的必要信息：关系起始点，关系终止点，关系属性

def run(driver,input1, input2,input3):
    driver.execute_query(input1 + "\n" + input2 + "\n" + input3, database_="neo4j", )
def print_friends(driver, name):
    records, _, _ = driver.execute_query(
        "MATCH (a:Person)-[:$KNOWS]->(friend) WHERE a.name = $name "
        "RETURN friend.name ORDER BY friend.name",
        name=name, database_="neo4j", KNOWS=name ,routing_=RoutingControl.READ,
    )
    for record in records:
        print(record["friend.name"])

def add_points(point_name,label='default'):
    base = "http://localhost:7474"

with GraphDatabase.driver(URI, auth=AUTH) as driver: 
    # add_friend(driver, "Arthur", "Guinevere")
    # add_friend(driver, "Arthur", "Lancelot")
    # add_friend(driver, "Arthur", "Merlin")
    # print_friends(driver, "Arthur")
    run(driver, add_point(driver,"test","a","学生","姓名","小明"),add_point(driver, "b", "学生", "姓名","小红"),add_relationship(driver,"a","b","同学"))