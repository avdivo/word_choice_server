from fastapi import FastAPI
from choice.word_choice import word_choice
from model.model import Filter
from fastapi.staticfiles import StaticFiles

# uvicorn main:app --reload

app = FastAPI()

app.mount("/5letters", StaticFiles(directory="static", html=True))

@app.post("/api/", response_model=dict())
def index(filter: Filter):
    li, t = word_choice(filter)
    return {'words': li, 'time': t}
