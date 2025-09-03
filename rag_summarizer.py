from transformers import BartForConditionalGeneration, BartTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from bs4 import BeautifulSoup
import re

def clean_text(html_text):
    """Clean HTML text by removing tags and extra whitespace."""
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, chunk_size=500):
    """Split text into chunks for RAG processing."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def create_rag_index(chunks):
    """Create a FAISS index for text chunks."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, show_progress_bar=False)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, model, chunks

def summarize_text(text, max_length=150, min_length=50):
    """Summarize text using BART."""
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    inputs = tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'],
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def rag_pipeline(html_text):
    """Run the RAG pipeline: clean, chunk, retrieve, and summarize."""
    # Clean the input HTML text
    cleaned_text = clean_text(html_text)
    if not cleaned_text:
        return "Error: No valid text extracted from the document."
    
    # Chunk the text for retrieval
    chunks = chunk_text(cleaned_text)
    if not chunks:
        return "Error: Text is too short to summarize."
    
    # Create FAISS index and retrieve relevant chunks
    index, model, chunks = create_rag_index(chunks)
    query = "Summarize the key terms and conditions in plain language."
    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, k=3)  # Retrieve top 3 chunks
    relevant_chunks = [chunks[i] for i in indices[0]]
    
    # Combine relevant chunks and summarize
    combined_text = " ".join(relevant_chunks)
    summary = summarize_text(combined_text)
    return summary

if __name__ == "__main__":
    # Test the pipeline with sample text (replace with actual scraped text)
    sample_html = """
    <h1>Terms and Conditions</h1>
    <p>Welcome to our website. By using this site, you agree to comply with our terms. You must not use this site for illegal purposes. We may update these terms at any time without notice.</p>
    """
    summary = rag_pipeline(sample_html)
    print("Summary:", summary)