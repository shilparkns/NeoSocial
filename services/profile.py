from db.connection import run_query
from models.user import User


def get_profile(user_id: str):
    """
    Fetch a user's profile from Neo4j by id.
    Returns a User object or None.
    """
    query = """
    MATCH (u:User {id: $id})
    RETURN u.id AS id,
           u.name AS name,
           u.username AS username,
           u.email AS email,
           u.bio AS bio
    """
    res = run_query(query, {"id": user_id})

    if not res:
        return None

    r = res[0]
    return User(
        id=r["id"],
        name=r["name"],
        username=r["username"],
        email=r["email"],
        bio=r["bio"]
    )

def is_username_taken(username: str, exclude_id: str) -> bool:
    """
    Check if a username is used by someone else (excluding this user).
    """
    query = """
    MATCH (u:User {username: $username})
    WHERE u.id <> $id
    RETURN COUNT(u) AS count
    """
    res = run_query(query, {"username": username, "id": exclude_id})
    if not res:
        return False
    return res[0]["count"] > 0


def is_email_taken(email: str, exclude_id: str) -> bool:
    """
    Check if an email is used by someone else (excluding this user).
    """
    query = """
    MATCH (u:User {email: $email})
    WHERE u.id <> $id
    RETURN COUNT(u) AS count
    """
    res = run_query(query, {"email": email, "id": exclude_id})
    if not res:
        return False
    return res[0]["count"] > 0


def update_profile(user_id: str, new_name: str, new_email: str,
                   new_username: str, new_bio: str):
    """
    Update name, email, username, and bio.
    Returns updated User or None.
    """
    query = """
    MATCH (u:User {id: $id})
    SET u.name = $name,
        u.email = $email,
        u.username = $username,
        u.bio = $bio
    RETURN u.id AS id,
           u.name AS name,
           u.username AS username,
           u.email AS email,
           u.bio AS bio
    """
    res = run_query(query, {
        "id": user_id,
        "name": new_name,
        "email": new_email,
        "username": new_username,
        "bio": new_bio
    })

    if not res:
        return None

    r = res[0]
    return User(
        id=r["id"],
        name=r["name"],
        username=r["username"],
        email=r["email"],
        bio=r["bio"]
    )
