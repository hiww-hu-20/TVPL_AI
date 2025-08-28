#!/usr/bin/env bash
set -euo pipefail

# 1) Đợi Qdrant sẵn sàng
echo "Waiting for Qdrant at ${QDRANT_HOST:-qdrant}:${QDRANT_PORT:-6333} ..."
until curl -fsS "http://${QDRANT_HOST:-qdrant}:${QDRANT_PORT:-6333}/readyz" >/dev/null; do
  sleep 1
done
echo "Qdrant is ready."

# 2) Tiền xử lý dữ liệu (nếu có thư mục data)
if [ -d "/app/data" ]; then
  echo "Running preprocess_file.py ..."
  python /app/preprocess_file.py || true
else
  echo "No /app/data found, skipping preprocess."
fi

# 3) Index vào Qdrant
#echo "Indexing to Qdrant ..."
#python -u -m src.indexer

# 4) Chạy API
exec uvicorn src.api:app --host 0.0.0.0 --port 8000