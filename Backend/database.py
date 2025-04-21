from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.skill_ecosystem

def save_to_db(collection_name, data):
    collection = db[collection_name]
    collection.insert_one(data)
    print(f"Data saved to {collection_name}")
