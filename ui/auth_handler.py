from services.auth import register, login

def handle_register():
    print("\n=== Register ===")
    name = input("Name: ").strip()
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    result = register(name, username, email, password)

    if isinstance(result, dict) and "error" in result:
        print("Registration failed:", result["error"])
    else:
        print(f"Registered as {result.username}. You can now log in.")


def handle_login():
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = login(username, password)

    if user is None:
        print("Login failed: invalid username or password.")
        return None

    print(f"Welcome, {user.name}!")
    return user
