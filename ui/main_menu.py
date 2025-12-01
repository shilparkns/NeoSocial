from ui.auth_handler import handle_register, handle_login

def main_loop():
    """Main entry point: controls auth and logged-in flow."""
    current_user = None

    while True:
        if current_user is None:
            current_user, should_exit = show_auth_menu()
        else:
            current_user, should_exit = show_logged_in_menu(current_user)

        if should_exit:
            print("Goodbye!")
            break


def show_auth_menu():
    """Menu shown when no user is logged in."""
    print("\n=== Auth Menu ===")
    print("1) Register")
    print("2) Login")
    print("0) Exit")

    choice = input("> ").strip()

    if choice == "1":
        handle_register()
        return None, False

    elif choice == "2":
        user = handle_login()
        return user, False

    elif choice == "0":
        return None, True

    else:
        print("Invalid choice.")
        return None, False


def show_logged_in_menu(current_user):
    """Menu shown when a user is logged in."""
    print(f"\n=== Logged in as {current_user.username} ===")
    print("1) Show my info")
    print("0) Logout")

    choice = input("> ").strip()

    if choice == "1":
        print("\n--- My Profile ---")
        print(f"ID:       {current_user.id}")
        print(f"Name:     {current_user.name}")
        print(f"Username: {current_user.username}")
        print(f"Email:    {current_user.email}")
        print(f"Bio:      {current_user.bio}")
        return current_user, False

    elif choice == "0":
        print("Logged out.")
        return None, False

    else:
        print("Invalid choice.")
        return current_user, False
