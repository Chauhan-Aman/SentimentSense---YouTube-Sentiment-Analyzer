from fastapi import FastAPI
from service.api.api import main_router
from fastapi.middleware.cors import CORSMiddleware
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = FastAPI(title="Comment Toxicity Classifier")

app.include_router(main_router)

origins = [
    "http://127.0.0.1:5500",
    "https://youtube.com/",
    "http://127.0.0.1:7860"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"project": "Comment Toxicity Classifier"}
