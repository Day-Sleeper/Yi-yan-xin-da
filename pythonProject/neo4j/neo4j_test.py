from neo4j import GraphDatabase, RoutingControl
import neo4j_main_functions as nmf

if __name__ == "__main__":
    nmf.MAIN_DATA_ini('neo4j_local_data.json')
    nmf.user_login()
    with GraphDatabase.driver(nmf.URL, auth=nmf.AUTH) as driver:
        nmf.clear_all_data(driver)
        nmf.add_point(driver, "test", "姓名", "小明",
                      "学生", "性别", "男")
        nmf.add_point(driver, "test", "姓名", "小红",
                      "学生", "性别", "女")
        nmf.add_relationship(driver, "test", "小明", "小红",
                             "同学", "时期", "初中")
        nmf.MAIN_DATA_SAVE('neo4j_local_data.json')
