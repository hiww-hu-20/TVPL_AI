from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.retrieve import retrieve_similar_clauses
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

class SearchResultItem(BaseModel):
    dieu_key: str
    title: str
    file_name: str
    text_chunk: str
    score: float

@app.post("/search", response_model=List[SearchResultItem])
def search_clauses(request: SearchRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = retrieve_similar_clauses(query, top_k=5)
    response = []
    for res in results:
        payload = res.payload
        score = res.score
        metadata = payload.get("metadata", {})
        response.append(SearchResultItem(
            dieu_key=metadata.get("dieu_key", "Không có mã"),
            title=metadata.get("title", "Không có tiêu đề"),
            file_name=metadata.get("file_name", "Không rõ file"),
            text_chunk=payload.get("text_chunk", ""),
            score=score
        ))
    return response
