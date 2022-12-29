from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping/")
async def ping():
    return {"ping": "pong!"}


@app.get("/example/")
async def example():
    filename = "example"
    filepath = f"examples/{filename}.csv"
    return FileResponse(filepath)
