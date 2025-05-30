import os
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

from dotenv import load_dotenv
load_dotenv()

from src.preprocessing import chunk_text_recursive, segment_text_vn
from src.embedding import embed_text
from src.qdrant_utils import recreate_collection, upsert_batch_to_qdrant

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_DIM = os.getenv("VECTOR_DIM")

def main():
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    recreate_collection(client, COLLECTION_NAME, VECTOR_DIM)

    input_folder = "./output"
    points = []
    idx = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Processing file: {filename}")

            for dieu_key, dieu_val in data.items():
                title = dieu_val.get("title", "")
                text = dieu_val.get("text", "")
                raw_text = f'{title}. {text}'

                chunks = chunk_text_recursive(raw_text, chunk_size=512, chunk_overlap=64)
                print(f"{dieu_key} split into {len(chunks)} chunks")

                for chunk in chunks:
                    chunk_with_title = f"{title} {chunk}"
                    text_segmented = segment_text_vn(chunk_with_title)
                    vector = embed_text(text_segmented)

                    point = rest.PointStruct(
                        id=idx,
                        vector=vector.tolist(),
                        payload={
                            "text_chunk": chunk_with_title,
                            "metadata": {
                                "dieu_key": dieu_key,
                                "title": title,
                                "file_name": filename
                            }
                        }
                    )
                    points.append(point)
                    idx += 1

            upsert_batch_to_qdrant(client, points, COLLECTION_NAME)
            points = []

    print(f"Finished upserting all data to Qdrant.")

if __name__ == "__main__":
    main()
