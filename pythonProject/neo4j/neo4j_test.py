from neo4j import GraphDatabase, RoutingControl
import neo4j_main_functions as nmf

if __name__ == "__main__":
    nmf.MAIN_DATA_ini('neo4j_local_data.json')
    nmf.user_login()
    with GraphDatabase.driver(nmf.URL, auth=nmf.AUTH) as driver:
        nmf.clear_all_data(driver)
        attribute_min = {"性别": "男", "祖籍": "江苏"}
        attribute_hong = {"性别": "女", "祖籍": "上海"}
        attribute_relation = {"时期": "初中", "学校": "地方中学"}
        nmf.add_point(driver, "test", "姓名", "小明",
                      "学生", attribute_min)
        nmf.add_point(driver, "test", "姓名", "小红",
                      "学生", attribute_hong)
        nmf.add_relationship(driver, "test", "小明", "小红",
                             "同学", attribute_relation)
        nmf.add_attribute(driver, "test", "小明", "年龄", "30")
        nmf.MAIN_DATA_SAVE('neo4j_local_data.json')
