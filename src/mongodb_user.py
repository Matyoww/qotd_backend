from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_user = os.getenv("MONGODB_USER")
print(mongodb_user)
mongodb_pass = os.getenv("MONGODB_PASS")

uri = f"mongodb+srv://{mongodb_user}:{mongodb_pass}@qotdcluster.lxdq3.mongodb.net/?retryWrites=true&w=majority&appName=qotdCluster"

class mongoDBManager:
    def __init__(self):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['qotd']
        self.collection = self.db['questions']

    def get_all_questions(self):
        questions = list(self.collection.find({}))
        for question in questions:
            question["_id"] = str(question["_id"])
        return questions

    def create_question(self, category: str, question: str):
        qid_collection = self.db['qid_sequence']
        id_counter = qid_collection.find_one_and_update(
            {"_id" : "qid_seq"},
            {"$inc" : {"qid_counter" : 1}},
            upsert=True,
            return_document=True
        )
        self.collection.insert_one({
            "qid" : id_counter['qid_counter'],
            "category" : category,
            "question": question}
        )

    def update_question(self, question_id: int, question: str):
        self.collection.update_one({"qid": question_id}, {"$set": {"question": question}})

    def delete_question(self, question_id: int):
        self.collection.delete_one({"qid": question_id})

    def get_number_of_questions(self):
        return self.collection.count_documents({})

    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
