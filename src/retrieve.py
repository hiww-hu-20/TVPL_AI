from qdrant_client import QdrantClient
from src.preprocessing import segment_text_vn
from src.embedding import embed_text

import os
from dotenv import load_dotenv
load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
TOP_K = int(os.getenv("TOP_K"))

def retrieve_similar_clauses(question, top_k=TOP_K):
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    question_processed = segment_text_vn(question)
    vector = embed_text(question_processed)
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector.tolist(),
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )
    return search_result

if __name__ == "__main__":
    question = "Hợp đồng lao động được giao kết theo hình thức nào?"  
    results = retrieve_similar_clauses(question)
    print(f"Tìm thấy {len(results)} kết quả liên quan:\n")
    for i, res in enumerate(results):
        payload = res.payload
        score = res.score
        
        metadata = payload.get("metadata", {})
        dieu_key = metadata.get("dieu_key", "Không có mã")
        title = metadata.get("title", "Không có tiêu đề")
        file_name = metadata.get("file_name", "Không rõ file")
        text_chunk = payload.get("text_chunk", "")

        print(f"Kết quả {i+1}:")
        print(f"  Mã điều khoản: {dieu_key}")
        print(f"  Tiêu đề: {title}")
        print(f"  File nguồn: {file_name}")
        print(f"  Nội dung: {text_chunk}")
        print(f"  Similarity: {score:.4f}")
        print("----\n")
