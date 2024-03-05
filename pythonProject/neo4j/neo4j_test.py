from neo4j import GraphDatabase, RoutingControl
import neo4j_database_ini as ndi
import neo4j_main_functions as nmf

if __name__ == "__main__":
    with GraphDatabase.driver(nmf.URI, auth=nmf.AUTH) as driver:
        nmf.clear_all_data(driver)
        ndi.initial_data("test")
        nmf.add_point(driver, "test", "小明", "学生",
                  "姓名", "小明", "性别", "男")
        nmf.add_point(driver, "test", "小红", "学生",
                  "姓名", "小红", "性别", "女")
        nmf.add_relationship(driver, "test", "小明", "小红",
                         "同学","时期", "初中" )
