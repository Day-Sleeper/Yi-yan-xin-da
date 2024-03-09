# -*- coding: utf-8 -*-
from neo4j import GraphDatabase


class Neo4jApp:
    URL = "bolt://localhost:7687"
    AUTH = ("neo4j", "ai123hr456")

    def __init__(self):
        self.URL = "bolt://localhost:7687"
        self.AUTH = ("neo4j", "ai123hr456")
        pass

    with GraphDatabase.driver(URL, auth=AUTH) as driver:
        def operation(self):
            pass

        def commit(self):
            pass

        def test(self):
            pass
