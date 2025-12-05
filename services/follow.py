from db.connection import run_query
from models.user import User

def follow_user(current_user_id: str, target_username: str):
    """
    UC-5: Follow another user.
    current_user_id follows user with target_username.
    Returns None on success, or {"error": "..."} on failure.
    """

    # Prevent following self by username lookup
    query = """
    MATCH (me:User {id: $meId})
    MATCH (target:User {username: $username})
    RETURN me.id AS meId, target.id AS targetId
    """
    res = run_query(query, {"meId": current_user_id, "username": target_username})

    if not res:
        return {"error": "User not found."}

    record = res[0]
    if record["meId"] == record["targetId"]:
        return {"error": "You cannot follow yourself."}
    
    # Check if already following
    query = """
    MATCH (me:User {id: $meId})-[r:FOLLOWS]->(target:User {username: $username})
    RETURN COUNT(r) AS count
    """
    res = run_query(query, {"meId": current_user_id, "username": target_username})
    if res and res[0]["count"] > 0:
        return {"error": "You are already following this user."}

    # Create FOLLOWS relationship
    query = """
    MATCH (me:User {id: $meId})
    MATCH (target:User {username: $username})
    MERGE (me)-[r:FOLLOWS]->(target)
    RETURN target.username AS username
    """
    res = run_query(query, {"meId": current_user_id, "username": target_username})

    if not res:
        return {"error": "Failed to follow user."}

    return None  # success


def unfollow_user(current_user_id: str, target_username: str):
    """
    UC-6: Unfollow a user.
    Removes FOLLOWS relation if it exists.
    Returns None on success, or {"error": "..."} on failure.
    """

    # 1) Ensure both me and target exist
    query = """
    MATCH (me:User {id: $meId})
    MATCH (target:User {username: $username})
    RETURN me.id AS meId, target.id AS targetId, target.username AS username
    """
    res = run_query(query, {"meId": current_user_id, "username": target_username})

    if not res:
        return {"error": "User not found."}

    record = res[0]

    # 2) Prevent unfollowing self
    if record["meId"] == record["targetId"]:
        return {"error": "You cannot unfollow yourself."}

    # 3) Delete relationship (if it exists)
    query = """
    MATCH (me:User {id: $meId})-[r:FOLLOWS]->(target:User {username: $username})
    DELETE r
    RETURN COUNT(r) AS deletedCount
    """
    res = run_query(query, {"meId": current_user_id, "username": target_username})

    deleted = res[0]["deletedCount"] if res else 0

    # 4) Handle case where there was nothing to unfollow
    if deleted == 0:
        return {"error": "You are not following this user."}

    return None  # success

# UC-7 - View Friends/Connections
def get_following(current_user_id: str):
    """
    This function show people I follow.
    I follow many user maybe, or maybe zero.
    If zero, return empty list. (I no follow anybody)
    """
    query = """
    MATCH (me:User {id: $meId})-[:FOLLOWS]->(u:User)
    RETURN u.id AS id, u.username AS username, u.name AS name
    ORDER BY username
    """
    res = run_query(query, {"meId": current_user_id})
    return res or []   # if nothing, give empty list

def get_followers(current_user_id: str):
    """
    This function show people who follow me.
    Maybe nobody follow me, then empty list.
    """
    query = """
    MATCH (u:User)-[:FOLLOWS]->(me:User {id: $meId})
    RETURN u.id AS id, u.username AS username, u.name AS name
    ORDER BY username
    """
    res = run_query(query, {"meId": current_user_id})
    return res or []   # return empty list if no follower

def get_connections(current_user_id: str):
    """
    UC-7 total function.
    I want see both list:
       - people I follow
       - people who follow me
    Return both together in dictionary.
    """
    following = get_following(current_user_id)
    followers = get_followers(current_user_id)

    return {
        "following": following,
        "followers": followers
    }

    # UC-8: find common follow between me and another user
def get_mutual_connections(current_user_id: str, target_username: str):
    # first check target user exists
    query = """
    MATCH (t:User {username: $username})
    RETURN t.id AS id
    """
    res = run_query(query, {"username": target_username})

    if not res:
        return {"error": "Target user not found."}

    target_user_id = res[0]["id"]

    # prevent checking with myself
    if target_user_id == current_user_id:
        return {"error": "Cannot check mutual with yourself."}

    # now find mutual follow
    query = """
    MATCH (me:User {id: $meId})-[:FOLLOWS]->(u:User)
    MATCH (t:User {id: $targetId})-[:FOLLOWS]->(u)
    RETURN u.id AS id, u.username AS username, u.name AS name
    ORDER BY username
    """
    mutuals = run_query(query, {"meId": current_user_id, "targetId": target_user_id})

    # mutuals might be empty list, it's ok
    return mutuals


def get_friend_recommendations(user_id, limit=10):
    query = """
    MATCH (u:User {id: $user_id})-[:FOLLOWS]->(mid:User)-[:FOLLOWS]->(rec:User)
    WHERE rec <> u
    AND NOT (u)-[:FOLLOWS]->(rec)
    WITH rec, count(DISTINCT mid) AS mutualConnections
    RETURN rec {
    .id,
    .username,
    .name,
    .email,
    .bio
    } AS userData,
    mutualConnections
    ORDER BY mutualConnections DESC, userData.username
    LIMIT $limit
    """

    result = run_query(query, {"user_id": user_id, "limit": limit})

    out = []
    for row in result:
        data = row["userData"]
        score = row["mutualConnections"]

        user = User(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            email=data["email"],
            bio=data.get("bio", "")
        )

        out.append({"user": user, "score": score})

    return out



def get_popular_users(limit=10):
    """
    UC-11: Explore Popular Users

    Returns the most-followed users with their follower counts.
    """
    query = """
    MATCH (u:User)
    OPTIONAL MATCH (u)<-[f:FOLLOWS]-(:User)
    WITH u, count(f) AS followers
    RETURN u {
      .id,
      .username,
      .name,
      .email,
      .bio
    } AS userData,
    followers
    ORDER BY followers DESC, userData.username
    LIMIT $limit
    """

    result = run_query(query, {"limit": limit})

    out = []
    for row in result:
        data = row["userData"]
        followers = row["followers"]

        user = User(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            email=data["email"],
            bio=data.get("bio", "")
        )

        out.append({"user": user, "followers": followers})

    return out