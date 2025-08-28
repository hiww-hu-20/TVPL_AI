FROM python:3.10-slim

WORKDIR /app

# Cài wget để tải file
RUN apt-get update && apt-get install -y \
    wget \
    curl\
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Tải VnCoreNLP model vào thư mục models

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./output ./output
COPY ./models ./models
COPY ./VnCoreNLP-1.2.jar ./VnCoreNLP-1.2.jar
COPY ./preprocess_file.py ./preprocess_file.py
COPY ./start.sh ./start.sh

EXPOSE 8000

CMD ["./start.sh"]