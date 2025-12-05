from services.follow import follow_user, unfollow_user, get_connections, get_mutual_connections, get_friend_recommendations, get_popular_users

def handle_follow(current_user):
    print("\n=== Follow User ===")
    username = input("Enter the username to follow: ").strip()

    if username == "":
        print("Username cannot be empty.")
        return

    result = follow_user(current_user.id, username)

    if isinstance(result, dict) and "error" in result:
        print("Could not follow user:", result["error"])
    else:
        print(f"You are now following '{username}'.")


def handle_unfollow(current_user):
    print("\n=== Unfollow User ===")
    username = input("Enter the username to unfollow: ").strip()

    if username == "":
        print("Username cannot be empty.")
        return

    result = unfollow_user(current_user.id, username)

    if isinstance(result, dict) and "error" in result:
        print("Could not unfollow user:", result["error"])
    else:
        print(f"You have unfollowed '{username}'.")


def handle_view_connections(current_user):
    # this function show my connection

    print("\n=== View My Connections ===")

    data = get_connections(current_user.id)

    # show following list
    print("People I follow:")
    if len(data["following"]) == 0:
        print("I follow nobody ... sad")
    else:
        for person in data["following"]:
            print(f" - {person['name']} @{person['username']}")

    # show followers list
    print("\nPeople who follow me:")
    if len(data["followers"]) == 0:
        print("No one follows me ... T_T")
    else:
        for person in data["followers"]:
            print(f" - {person['name']} @{person['username']}")

def handle_mutual_connections(current_user):
    # this function show mutual follow between me and other user (sorry english bad)

    print("\n=== Mutual Connections (UC-8) ===")
    username = input("Enter username to check mutuals: ").strip()

    if username == "":
        print("Username cannot be empty.")
        return

    result = get_mutual_connections(current_user.id, username)

    # error case
    if isinstance(result, dict) and "error" in result:
        print("Error:", result["error"])
        return

    # empty list → no mutual
    if len(result) == 0:
        print("No mutuals found.")
        return

    print(f"\nYou and {username} both follow these users:")
    for user in result:
        print(f" - {user['username']} @{user['name']}")

def handle_friend_recommendations(current_user):
    print("\n=== Friend Recommendations ===")

    recs = get_friend_recommendations(current_user.id, limit=10)

    if not recs:
        print("No recommendations available.")
        return

    for item in recs:
        user = item["user"]
        score = item["score"]
        print(f"{user.name} @{user.username} |  Mutual connections: {score}")


def handle_popular_users(current_user):
    """
    UC-11: Explore Popular Users
    """
    print("\n=== Popular Users ===")

    popular = get_popular_users(limit=10)

    if not popular:
        print("No users found.")
        return

    for rank, item in enumerate(popular, start=1):
        user = item["user"]
        followers = item["followers"]
        print(f" #{rank} {user.name} @{user.username} | Followers: {followers}")



