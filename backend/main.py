from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from prediction import predict


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


@app.post("/upload/")
async def inputs(file: UploadFile, includesN: bool = Form()):
    print(includesN)
    print(predict(file.file))
    return {"filename": file.filename}
