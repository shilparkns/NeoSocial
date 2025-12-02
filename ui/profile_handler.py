from services.profile import (
    get_profile,
    update_profile,
    is_email_taken,
    is_username_taken,
)


def handle_view_profile(current_user):
    """
    Fetch and print the latest profile info for the current user.
    """
    profile = get_profile(current_user.id)

    if profile is None:
        print("Could not load profile.")
        return

    print("\n--- My Profile ---")
    print(f"ID:       {profile.id}")
    print(f"Name:     {profile.name}")
    print(f"Username: {profile.username}")
    print(f"Email:    {profile.email}")
    print(f"Bio:      {profile.bio}")

def _is_valid_email(email: str) -> bool:
    if "@" not in email:
        return False
    local, _, domain = email.partition("@")
    return bool(local and "." in domain)


def handle_edit_profile(current_user):
    profile = get_profile(current_user.id)
    if profile is None:
        print("Could not load profile.")
        return current_user

    print("\n=== Edit Profile ===")
    print("Press Enter to keep the current value.")
    print("For bio: type '-' to clear it.\n")

    # ---- Name ----
    name_input = input(f"Name [{profile.name}]: ").strip()
    if name_input == "":
        new_name = profile.name
    else:
        new_name = name_input

    # ---- Email ----
    email_input = input(f"Email [{profile.email}]: ").strip()
    if email_input == "":
        new_email = profile.email
    else:
        new_email = email_input
        # validate format if changed
        if not _is_valid_email(new_email):
            print("Invalid email format. No changes made.")
            return current_user
        # check if taken (only if changed)
        if is_email_taken(new_email, profile.id):
            print("That email is already in use. No changes made.")
            return current_user

    # ---- Username ----
    username_input = input(f"Username [{profile.username}]: ").strip()
    if username_input == "":
        new_username = profile.username
    else:
        new_username = username_input
        # check if taken (only if changed)
        if is_username_taken(new_username, profile.id):
            print("That username is already taken. No changes made.")
            return current_user

    # ---- Bio ----
    bio_input = input(f"Bio [{profile.bio}]: ").strip()
    if bio_input == "":
        new_bio = profile.bio          # keep
    elif bio_input == "-":
        new_bio = ""                   # clear
    else:
        new_bio = bio_input            # update

    # ---- Abort if nothing changed ----
    if (
        new_name == profile.name and
        new_email == profile.email and
        new_username == profile.username and
        new_bio == profile.bio
    ):
        print("No changes made.")
        return current_user

    # ---- Save changes ----
    updated = update_profile(
        profile.id,
        new_name,
        new_email,
        new_username,
        new_bio
    )

    if updated is None:
        print("Failed to update profile.")
        return current_user

    print("Profile updated successfully.")
    return updated
