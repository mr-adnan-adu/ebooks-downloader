from pymongo import MongoClient
from info import FILES_DATABASE_URL

client = MongoClient(FILES_DATABASE_URL)
db = client["ebooks_db"]
ebooks_collection = db["ebooks"]
bans_collection = db["bans"]
users_collection = db["users"]

ebooks_collection.create_index([("title", "text"), ("author", "text"), ("genre", "text")])
