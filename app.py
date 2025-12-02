from neo4j import GraphDatabase
import hashlib

# DB connection class
class DB:
    def __init__(self):
        # TODO: change password before submitting lol
        self.driver = GraphDatabase.driver(
    "neo4j+s://d2c03461.databases.neo4j.io",
    auth=("neo4j", "2BURMyukNOm3H1gDDph65CibWEF8KqUq5H1oIX_GxFs")
)


    def run(self, query, params=None):
        # new session every time... kinda slow but whatever
        with self.driver.session() as session:
            return session.run(query, params or {}).data()

# Utility function for hashing passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register new user
def register(db):
    print("=== Register ===")
    name = input("Name: ")
    username = input("Username: ")
    email = input("Email: ")
    pw = input("Password: ")

    query = """
    CREATE (u:User {
        id: randomUUID(),
        name: $name,
        username: $username,
        email: $email,
        bio: "",
        passwordHash: $pwHash
    })
    RETURN u
    """

    result = db.run(query, {
        "name": name,
        "username": username,
        "email": email,
        "pwHash": hash_password(pw)
    })

    if result:
        print("Registration successful!")
    else:
        print("Something broke... maybe try again")

# Login
def login(db):
    print("=== Login ===")
    username = input("Username: ")
    pw = input("Password: ")

    query = """
    MATCH (u:User {username:$u})
    RETURN u
    """

    result = db.run(query, {"u": username})

    if not result:
        print("No such username...")
        return None

    user = result[0]["u"]

    if user["passwordHash"] == hash_password(pw):
        print("Login OK!")
        return user
    else:
        print("Wrong password...")
        return None
    
    # prodile funtion
def view_profile(user):
    print("=== My Profile ===")
    print("Name:", user.get("name"))
    print("Username:", user.get("username"))
    print("Email:", user.get("email"))
    print("Bio:", user.get("bio"))

def edit_profile(db, user):
    print("=== Edit Profile ===")
    new_name = input("New name: ")
    new_email = input("New email: ")
    new_bio = input("New bio: ")

    query = """
    MATCH (u:User {id:$id})
    SET u.name = $name,
        u.email = $email,
        u.bio = $bio
    RETURN u
    """

    result = db.run(query, {
        "id": user["id"],
        "name": new_name,
        "email": new_email,
        "bio": new_bio
    })

    if result:
        print("Profile updated!")
        return result[0]["u"]
    else:
        print("Update failed...")
        return user
    
# Follow / Unfollow

def follow(db, user):
    print("=== Follow someone ===")
    target_id = input("Enter target user ID: ")

    query = """
    MATCH (a:User {id:$me})
    MATCH (b:User {id:$target})
    MERGE (a)-[:FOLLOWS {since:date()}]->(b)
    """

    db.run(query, {"me": user["id"], "target": target_id})
    print("Followed (probably)")


def unfollow(db, user):
    print("=== Unfollow ===")
    target_id = input("Enter target user ID: ")

    query = """
    MATCH (a:User {id:$me})-[r:FOLLOWS]->(b:User {id:$target})
    DELETE r
    """

    db.run(query, {"me": user["id"], "target": target_id})
    print("Unfollowed (I think)")

# Viewing social connections    
def list_following(db, user):
    query = """
    MATCH (:User {id:$id})-[:FOLLOWS]->(other)
    RETURN other
    """
    result = db.run(query, {"id": user["id"]})
    print("=== People I follow ===")
    for r in result:
        print(r["other"])


def list_followers(db, user):
    query = """
    MATCH (other)-[:FOLLOWS]->(:User {id:$id})
    RETURN other
    """
    result = db.run(query, {"id": user["id"]})
    print("=== People who follow me ===")
    for r in result:
        print(r["other"])

# Mutual connections

def mutuals(db, user):
    other = input("Other user ID: ")

    query = """
    MATCH (me:User {id:$me})-[:FOLLOWS]->(x)<-[:FOLLOWS]-(u:User {id:$other})
    RETURN x
    """

    result = db.run(query, {"me": user["id"], "other": other})

    print("=== Mutual connections ===")
    for r in result:
        print(r["x"])

# Recommendations, Search, Popular Users
def recommendations(db, user):
    query = """
    MATCH (me:User {id:$id})-[:FOLLOWS]->(f)-[:FOLLOWS]->(rec)
    WHERE rec.id <> $id AND NOT (me)-[:FOLLOWS]->(rec)
    RETURN rec, COUNT(*) AS score
    ORDER BY score DESC LIMIT 10
    """
    result = db.run(query, {"id": user["id"]})

    print("=== Recommendations ===")
    for r in result:
        print(r["rec"], ", score:", r["score"])


def search_users(db):
    kw = input("Search keyword: ")
    query = """
    MATCH (u:User)
    WHERE toLower(u.name) CONTAINS toLower($k)
       OR toLower(u.username) CONTAINS toLower($k)
    RETURN u
    """
    result = db.run(query, {"k": kw})
    print("=== Search Results ===")
    for r in result:
        print(r["u"])


def popular_users(db):
    query = """
    MATCH (u:User)<-[:FOLLOWS]-()
    RETURN u, COUNT(*) AS followers
    ORDER BY followers DESC LIMIT 10
    """
    result = db.run(query)

    print("=== Popular Users ===")
    for r in result:
        print(r["u"], "Followers:", r["followers"])

# Main app loop
def main():
    db = DB()
    current = None

    while True:
        if not current:
            print("\n===== Welcome to NeoSocial =====")
            print("1) Register")
            print("2) Login")
            print("0) Exit")

            choice = input("> ")

            if choice == "1":
                register(db)
            elif choice == "2":
                current = login(db)
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Invalid choice")

        else:
            print(f"\nLogged in as: {current['username']}")
            print("1) View Profile")
            print("2) Edit Profile")
            print("3) Follow someone")
            print("4) Unfollow")
            print("5) Show my following")
            print("6) Show my followers")
            print("7) Mutual connections")
            print("8) Recommendations")
            print("9) Search users")
            print("10) Popular users")
            print("0) Logout")

            choice = input("> ")

            if choice == "1":
                view_profile(current)
            elif choice == "2":
                current = edit_profile(db, current)
            elif choice == "3":
                follow(db, current)
            elif choice == "4":
                unfollow(db, current)
            elif choice == "5":
                list_following(db, current)
            elif choice == "6":
                list_followers(db, current)
            elif choice == "7":
                mutuals(db, current)
            elif choice == "8":
                recommendations(db, current)
            elif choice == "9":
                search_users(db)
            elif choice == "10":
                popular_users(db)
            elif choice == "0":
                current = None
            else:
                print("Invalid input...")

if __name__ == "__main__":
    main()

    from db.connection import run_query

print(run_query("RETURN 'Neo4j works!' AS msg"))
