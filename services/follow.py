from db.connection import run_query

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

