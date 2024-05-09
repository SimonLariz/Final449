from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient("localhost", 27017)

db = client["database"]

users_collection = db["users"]
food_collection = db["food"]


# USER CRUD OPERATIONS
def create_user(username, password):
    user = {"username": username, "password": password, "created_at": datetime.now()}
    users_collection.insert_one(user)


def get_user(username):
    return users_collection.find_one({"username": username})


def get_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})


def update_user_username(user_id, new_username):
    users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"username": new_username}}
    )


def update_user_password(user_id, new_password):
    users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"password": new_password}}
    )


def delete_user(user_id):
    users_collection.delete_one({"_id": ObjectId(user_id)})


def get_all_users():
    return users_collection.find({})


print("Connected to MongoDB")
print("Database:", db)

print("Users in the database:")
for user in get_all_users():
    print(user)
