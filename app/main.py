from fastapi import FastAPI
from starlette.responses import RedirectResponse

from choice.word_choice import word_choice
from model.model import Filter
from fastapi.staticfiles import StaticFiles

# uvicorn main:app --reload

app = FastAPI()

app.mount("/5letters/", StaticFiles(directory="static", html=True))

@app.post("/5/api/", response_model=dict())
def index(filter: Filter):
    li, t = word_choice(filter)
    return {'words': li, 'time': t}

@app.get("/")
def redirect():
    response = RedirectResponse(url='5letters')  # Если вход в корень сайта, редирект к программе
    return response