from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

MERRIAM_WEBSTER_API_KEY = os.getenv("MW_API_KEY")

class WordRequest(BaseModel):
    word: str

@app.post("/define")
def define_word(req: WordRequest):
    if not MERRIAM_WEBSTER_API_KEY:
        return {"error": "API key not set"}
    url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{req.word}?key={MERRIAM_WEBSTER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data and isinstance(data[0], dict):
            defs = data[0].get("shortdef", [])
            return {"definitions": defs}
    return {"error": "No definition found"}
