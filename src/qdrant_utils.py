from qdrant_client.http import models as rest

def recreate_collection(client, collection_name, vector_dim):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=rest.VectorParams(size=vector_dim, distance=rest.Distance.COSINE)
    )
    print(f"Created collection '{collection_name}' in Qdrant.")

def upsert_batch_to_qdrant(client, points, collection_name, batch_size=10):
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=collection_name, points=batch)
        print(f"Upserted batch {i // batch_size + 1} ({len(batch)} points)")


