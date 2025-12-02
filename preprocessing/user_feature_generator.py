import csv, random
import hashlib

EDGES_IN = "data/follows.csv"
USERS_OUT = "data/users.csv"


def generate_bio(name):
    interests = [
        "coding", "music", "traveling", "gaming", "reading",
        "photography", "fitness", "technology", "design",
        "coffee", "movies", "sports", "art", "nature",
        "food", "science", "AI", "startups", "blogging",
        "learning new things"
    ]

    vibes = [
        "lover", "enthusiast", "nerd", "fan", "explorer",
        "creator", "builder", "dreamer", "thinker", "wanderer"
    ]

    extras = [
        "Always learning.",
        "Trying to get better every day.",
        "Living life one line of code at a time.",
        "Here to connect and share ideas.",
        "Passionate about what I do.",
        "Curious mind, open heart.",
        "Be kind. Always.",
        "Let's build something cool.",
        "Coffee-powered human.",
        "Creating my own path."
    ]

    interest = random.choice(interests)
    vibe = random.choice(vibes)
    extra = random.choice(extras)

    return f"{name}. {interest.capitalize()} {vibe}. {extra}"


# 100-ish first & last names (shortened list – add more if you like)
first_names = [
    "Liam","Noah","Oliver","Elijah","James","William","Benjamin","Lucas","Henry","Alexander",
    "Emma","Olivia","Ava","Sophia","Isabella","Mia","Charlotte","Amelia","Harper","Evelyn",
    "Ethan","Mason","Logan","Jacob","Michael","Daniel","Aiden","Jackson","Sebastian","Jack",
    "Emily","Abigail","Elizabeth","Sofia","Avery","Ella","Scarlett","Grace","Chloe","Victoria",
    "David","Joseph","Carter","Wyatt","Jayden","John","Owen","Dylan","Luke","Gabriel",
    "Hannah","Lily","Natalie","Zoe","Nora","Riley","Lillian","Hazel","Aurora","Penelope",
    "Caleb","Isaac","Samuel","Hunter","Christian","Levi","Mateo","Julian","Grayson","Leo",
    "Aria","Layla","Ellie","Stella","Lucy","Claire","Violet","Savannah","Audrey","Brooklyn",
    "Andrew","Thomas","Charles","Jaxon","Ezra","Hudson","Nicholas","Jeremiah","Elias","Miles",
    "Paisley","Skylar","Naomi","Genesis","Isla","Elena","Caroline","Anna","Sarah","Allison"
]

last_names = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
    "Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes",
    "Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper",
    "Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson",
    "Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes",
    "Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez"
]

# 1) collect node IDs from the edge file
node_ids = set()
with open(EDGES_IN, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        node_ids.add(row["fromId"])
        node_ids.add(row["toId"])

node_ids = list(node_ids)

# 2) build profiles
rows = []
for i, nid in enumerate(node_ids):
    fn = first_names[i % len(first_names)]
    ln = last_names[(i // len(first_names)) % len(last_names)]
    name = f"{fn} {ln}"

    base_username = (fn[0] + ln).lower()   # e.g. "lsmith"
    username = f"{base_username}{i % 1000}"  # add number to avoid duplicates
    email = f"{username}@gmail.com"

    bio = generate_bio(name)
    raw_password = f"{base_username}pass123" 
    password = hashlib.sha256(raw_password.encode()).hexdigest()

    rows.append([nid, name, username, email, bio, password])

# 3) write users_1500.csv
with open(USERS_OUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["userId", "name", "username", "email", "bio", "password"])
    writer.writerows(rows)

print(f"Generated {len(rows)} users.")
