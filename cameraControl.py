from fastapi import FastAPI

@app.get("/take_photo")
def read_root():
    return {"Hello": "World"}