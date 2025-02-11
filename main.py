from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"data": {'name': 'Drew'}}

@app.get("/about")
def about():
    return {"message": "About page"}