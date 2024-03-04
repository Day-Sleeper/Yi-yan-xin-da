from neo4j import GraphDatabase, RoutingControl

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ai123hr456")

"""
所有点数据必须要包含至少一个属性为其名称/姓名/name等
"""


"""
MATCH (a:学生),(b:学生) WHERE a.姓名 = '小明' AND b.姓名 = '小红';
CREATE (a)-[r:'同学']->(b)
"""
def initial_data(database_name):
    global main_data
    main_data = {}
    point_data = {}
    classification_data = {}
    relationship_data = {}
    classification_data["点数据"] = point_data
    classification_data["边数据"] = relationship_data
    main_data[database_name] =classification_data

def search_point(database_name,point_name):
    for key in main_data[database_name]["点数据"][point_name].keys:
        pass

def clear_all_data(driver):
    """
    调试使用：清除数据库内所有数据
    """
    driver.execute_query("match (n) detach delete n", database_="neo4j", )

def add_point(driver, database_name, point_name, main_label, name_call, name, attribute_name, attribute_value,):
    # 节点必要信息信息：节点名称，主要标签，一个属性名称和属性值（均可以为中文）
    input_cyphel = "CREATE ({point_name}:{main_label} {{ {name_call}: '{name}', {attribute_name}: '{attribute_value}' }}) "\
        .format(point_name=point_name,
                main_label=main_label,
                attribute_name=attribute_name,
                attribute_value=attribute_value,
                name_call=name_call,
                name=name)
    main_data[database_name]["点数据"][point_name] = {"名称叫法":name_call,
                                                      name_call: name,
                                                      "主标签": main_label,
                                                      attribute_name: attribute_value}
    driver.execute_query(input_cyphel, database_="neo4j",)


def add_relationship(driver, database_name, relationship_start, relationship_end, relationship_label, attribute_name, attribute_value):
    # 关系的必要信息：关系起始点，关系终止点，关系属性
    input_cyphel = """
    MATCH ({relationship_start}:{relationship_start_main_label}),({relationship_end}:{relationship_end_main_label})
    WHERE {relationship_start}.{relationship_start_name_call} = {relationship_start} AND {relationship_end}.{relationship_end_name_call} = {relationship_end}
    CREATE ({relationship_start})-[关系:{relationship_label}]->({relationship_end})
    """.format(relationship_start=relationship_start,
                relationship_end=relationship_end,
                relationship_start_main_label=main_data[database_name]["点数据"][relationship_start]["主标签"],
                relationship_end_main_label=main_data[database_name]["点数据"][relationship_end]["主标签"],
                relationship_start_name_call=main_data[database_name]["点数据"][relationship_start]["名称叫法"],
                relationship_end_name_call=main_data[database_name]["点数据"][relationship_end]["名称叫法"],
                relationship_label=relationship_label)
    main_data[database_name]["边数据"][relationship_label] = {"主标签": relationship_label,
                                                            attribute_name: attribute_value}
    driver.execute_query(input_cyphel, database_="neo4j",)



if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        clear_all_data(driver)
        initial_data("test")
        add_point(driver, "test", "小明", "学生",
                  "姓名", "小明", "性别", "男")
        add_point(driver, "test", "小红", "学生",
                  "姓名", "小红", "性别", "女")
        add_relationship(driver, "test", "小明", "小红",
                         "同学","时期", "初中" )
