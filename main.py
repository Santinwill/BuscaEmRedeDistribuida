import json
from bson import json_util
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic_settings import BaseSettings
from functools import lru_cache
import httpx
import asyncio

class Environment(BaseSettings):
    database_name: str = ""
    mongo_uri: str = ""
    vizinhos: list[str] = []

    class Config:
        env_file = ".env"

@lru_cache()
def get_environment() -> Environment:
    return Environment()

app = FastAPI()

async def dfs_search(_id: str, visited: set, original: bool = True) -> dict:
    env = get_environment()
    if original:
        visited = set()

    mongo_client = MongoClient(env.mongo_uri)
    database = mongo_client[env.database_name]
    collection = database["listingsAndReviews"]
    document = collection.find_one({"_id": _id})

    if document:
        return json.loads(json_util.dumps(document))

    async with httpx.AsyncClient() as client:
        tasks = []
        for vizinho in env.vizinhos:
            if vizinho not in visited:
                visited.add(vizinho)
                url = f"http://{vizinho}/api/{_id}?visited={','.join(visited)}"
                task = client.get(url)
                tasks.append(task)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            if isinstance(response, httpx.Response) and response.status_code == 200:
                return response.json()

    if original:
        raise HTTPException(status_code=404, detail="documento nao encontrado")

@app.get("/api/{_id}")
async def get_review(_id: str, visited: str = ""):
    visited_set = set(visited.split(',')) if visited else set()
    result = await dfs_search(_id, visited_set)
    return result
