import torch
from transformers import AutoTokenizer, RobertaModel
import os

from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = MODEL_NAME = os.getenv("MODEL_NAME")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = RobertaModel.from_pretrained(MODEL_NAME)
model.eval()



def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings[0].detach().numpy()


