from neo4j import GraphDatabase

# Neo4j Connection Config
URI = "neo4j+s://d2c03461.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "2BURMyukNOm3H1gDDph65CibWEF8KqUq5H1oIX_GxFs"

# Driver Initialization
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
driver.verify_connectivity()

# Query Helper 
def run_query(query, params=None):
    if params is None:
        params = {}

    with driver.session() as session:
        result = session.run(query, params)
        return list(result)

# Cleanup 
def close_driver():
    driver.close()
    