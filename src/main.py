from fastapi import FastAPI
import random
import json

app = FastAPI()

with open('data/questions.json', 'r') as file:
    questions = json.load(file)

@app.get("/question")
def read_quote():
    return random.choice(questions["questions"])

@app.get("/question/all")
def read_all_questions():
    return questions