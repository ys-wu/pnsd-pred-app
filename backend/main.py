from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/example/")
async def example():
    filename = "example"
    filepath = f"examples/{filename}.csv"
    return FileResponse(filepath)
