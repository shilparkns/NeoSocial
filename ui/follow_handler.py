from services.follow import follow_user, unfollow_user

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
