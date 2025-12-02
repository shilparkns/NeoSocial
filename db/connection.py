
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

# Neo4j Connection Config
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

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
    