import py_vncorenlp
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

py_vncorenlp.download_model(save_dir='./')

rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='./')


def chunk_text_recursive(text, chunk_size=512, chunk_overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    return splitter.split_text(text)

def segment_text_vn(text):
    segmented = rdrsegmenter.word_segment(text)
    return " ".join(segmented)
