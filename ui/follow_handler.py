from services.follow import follow_user, unfollow_user, get_connections

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
            print(f" - {person['username']}")

    # show followers list
    print("\nPeople who follow me:")
    if len(data["followers"]) == 0:
        print("No one follows me ... T_T")
    else:
        for person in data["followers"]:
            print(f" - {person['username']}")





