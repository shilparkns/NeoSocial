from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    username: str
    email: str
    bio: str