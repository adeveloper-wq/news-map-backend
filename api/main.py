from api.crawlers.crawler_cnn import CrawlerCNN
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pymongo import MongoClient
from bson.json_util import dumps
import json

client = MongoClient(os.environ["MONGODB_URL"])
db=client.news

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/{news_outlet}", status_code=200)
def get_coordinates(news_outlet: str = ""):
    if news_outlet == "cnn":
        """ CrawlerCNN.get_articles_from_month(db, "2022-02") """
        return JSONResponse(status_code=status.HTTP_200_OK, content=parse_json(list(db.cnn.find({}))))
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="News outlet not available.")
    
def parse_json(data):
    return json.loads(dumps(data))