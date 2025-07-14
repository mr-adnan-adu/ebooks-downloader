from pymongo import MongoClient
from info import FILES_DATABASE_URL

def get_db():
    client = MongoClient(FILES_DATABASE_URL)
    return client["ebooks_db"]["ebooks"]

def format_result(result):
    return (
        f"**Book**: {result['title']}\n"
        f"**Author**: {result['author']}\n"
        f"**Genre**: {result['genre']}\n"
        f"**Format**: {result['format']}\n"
        f"**Link**: [Download]({result['file_link']})"
    )
