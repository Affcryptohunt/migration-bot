from fastapi import FastAPI
from migrate import migrate_store

app = FastAPI()

@app.post("/scrape")
def scrape(url:str):
    result = migrate_store(url)
    return result