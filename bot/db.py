from pymongo import MongoClient

from user import User, State, WorkingState


client = MongoClient("localhost", 27017)
db = client["overvoice"]
users = db["users"]

def get_user(telegram_id: int) -> User:
    raw = users.find_one({"telegram_id": telegram_id})
    if raw is None:
        return None
    user = User(
        telegram_id=raw["telegram_id"],
        username=raw["username"],
        state=State(raw["state"]),
        voice=raw["voice"],
    )
    return user


def add_user(user: User) -> None:
    post_id = users.insert_one(user.tojson()).inserted_id


def update_user(user: User) -> None:
    result = users.update_one({"telegram_id": user.telegram_id}, {"$set": user.tojson()})
    if result.modified_count == 0:
        raise ValueError("User not found or update did not modify any documents")