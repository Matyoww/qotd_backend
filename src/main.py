from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongodb_user import mongoDBManager
import random

app = FastAPI()
db_mgr = mongoDBManager()

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:4200",
    "https://qotd-site.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/question", tags=["question"])
def read_question():
    questions = db_mgr.get_all_questions()
    questions = [question["question"] for question in questions]
    random_question = random.choice(questions)
    return random_question

@app.post("/question", tags=["question"])
def add_question(category: str, question: str):
    db_mgr.create_question(category, question)
    return {"status": "Question added successfully"}

@app.get("/question/all", tags=["question"])
def read_all_questions(include_meta: bool = True):
    questions = db_mgr.get_all_questions()
    if include_meta:
        return questions
    else:
        return [question["question"] for question in questions]

@app.get("/question/{question_id}", tags=["question"])
def read_question_by_id(question_id: int, include_meta: bool = True):
    question = db_mgr.collection.find_one({"qid": question_id})
    question["_id"] = str(question["_id"])

    if include_meta:
        return question
    else:
        return question["question"]

@app.put("/question/{question_id}", tags=["question"])
def update_question(question_id: int, question: str):
    db_mgr.update_question(question_id, question)
    return {"status": "Question updated successfully"}

@app.delete("/question/{question_id}", tags=["question"])
def delete_question(question_id: int):
    db_mgr.delete_question(question_id)
    return {"status": "Question deleted successfully"}