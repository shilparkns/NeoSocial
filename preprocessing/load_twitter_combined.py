from neo4j import GraphDatabase

URI = "neo4j+s://d2c03461.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "2BURMyukNOm3H1gDDph65CibWEF8KqUq5H1oIX_GxFs"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def load_edges():
    with driver.session() as session:
        with open("data/twitter_combined.txt", "r") as f:
            for line in f:
                u1, u2 = line.strip().split()
                session.run("""
                    MERGE (a:User {id:$u1})
                    MERGE (b:User {id:$u2})
                    MERGE (a)-[:FOLLOWS]->(b)
                """, {"u1": u1, "u2": u2})
    print("Finished loading graph!")

if __name__ == "__main__":
    load_edges()
    driver.close()
