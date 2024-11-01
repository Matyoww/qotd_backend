from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import json

app = FastAPI()

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

with open('data/questions.json', 'r') as file:
    questions = json.load(file)

@app.get("/question")
def read_quote():
    return random.choice(questions["questions"])

@app.get("/question/all")
def read_all_questions():
    return questions