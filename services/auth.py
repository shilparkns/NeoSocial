import hashlib
from db.connection import run_query
from models.user import User


# 1) Password hashing
def hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()

# 2) Get next numeric user ID
def get_next_user_id() -> str:
    query = """
    MATCH (u:User)
    RETURN max(toInteger(u.id)) AS maxId
    """
    res = run_query(query)

    if not res or res[0]["maxId"] is None:
        return "1"  # if no users exist

    max_id = res[0]["maxId"]
    return str(max_id + 1)


# 3) Check if username/email exists
def check_username_email_exists(username: str, email: str):
    query = """
                MATCH (u:User)
                WHERE u.username = $username OR u.email = $email
                RETURN u.username AS existingUsername,
                    u.email AS existingEmail
            """

    res = run_query(query, {"username": username, "email": email})
    return len(res) > 0


# 4) Register new user
def register(name, username, email, raw_password):
    # username check
    if check_username_email_exists(username, email):
        return {"error": "Username/email already taken."}

    # generate new ID + hash password
    new_id = get_next_user_id()
    password_hash = hash_password(raw_password)

    # insert into Neo4j
    query = """
    CREATE (u:User {
        id: $id,
        name: $name,
        username: $username,
        email: $email,
        bio: "I’m new here — excited to connect!",
        passwordHash: $passwordHash
    })
    RETURN u
    """

    res = run_query(query, {
        "id": new_id,
        "name": name,
        "username": username,
        "email": email,
        "passwordHash": password_hash
    })

    if not res:
        return {"error": "Registration failed."}

    u = res[0]["u"]

    return User(
        id=u["id"],
        name=u["name"],
        username=u["username"],
        email=u["email"],
        bio=u["bio"]
    )


# 5) Login


def login(username, raw_password):
    query = """
    MATCH (u:User {username: $username})
    RETURN u.passwordHash AS hash,
           u.id AS id,
           u.name AS name,
           u.username AS username,
           u.email AS email,
           u.bio AS bio
    """

    res = run_query(query, {"username": username})
    if not res:
        return None

    record = res[0]

    if hash_password(raw_password) != record["hash"]:
        return None

    return User(
        id=record["id"],
        name=record["name"],
        username=record["username"],
        email=record["email"],
        bio=record["bio"]
    )

if __name__ == "__main__":
    new_user = register("Alicia Scott", "alisea", "alicia.s@gmail.com", "alisea@socials")
    print("Registered:", new_user)
    logged_in_user = login("alisea", "alisea@socials")
    print("Logged in:", logged_in_user)    
    wrong_login = login("alisea", "wrongpassword")
    print("Wrong login (should be None):", wrong_login)