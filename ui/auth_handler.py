from services.auth import register, login

def _is_valid_email(email: str) -> bool:
    if "@" not in email:
        return False
    local, _, domain = email.partition("@")
    return bool(local and "." in domain)


def handle_register():
    print("\n=== Register ===")
    name = input("Name: ").strip()
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    if not _is_valid_email(email):
        print("Invalid email format.")
        return
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
