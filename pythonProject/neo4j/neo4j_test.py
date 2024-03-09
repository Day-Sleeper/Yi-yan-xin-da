from neo4j_functions import Neo4jApp

if __name__ == "__main__":
    App1 = Neo4jApp()

    App1.clear_all_data()
    attribute_min = {"性别": "男", "祖籍": "江苏"}
    attribute_hong = {"性别": "女", "祖籍": "上海"}
    attribute_relation = {"时期": "初中", "学校": "地方中学"}
    attribute_update1 = {"语文成绩": "A", "数学成绩": "B", "英语成绩": "C"}
    attribute_update2 = {"认识时间": "某年某月", "结束时间": "某年某月"}
    App1.add_point("姓名", "小明", "学生", attribute_min)
    App1.add_point("姓名", "小红", "学生", attribute_hong)
    App1.add_relationship("小明", "小红", "同学", attribute_relation)
    App1.add_point_attribute("test", "小明", attribute_update1)
    App1.add_relationship_attribute("test", "同学", "小明", "小红", attribute_update2)
    App1.main_data_SAVE()

