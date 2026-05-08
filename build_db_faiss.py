import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import pickle
import re

# -----------------------------
# Cleaning functions 🧹
# -----------------------------
def clean_sentence(s):
    s = s.strip()

    # remove small sentences
    if len(s) < 50:
        return None

    # remove junk patterns
    junk = [
        r"subscribe", r"advertisement", r"cookies", r"policy",
        r"sign in", r"login", r"follow us", r"newsletter",
        r"read more", r"copyright", r"©",
        r"breaking news", r"live updates"
    ]
    for j in junk:
        if re.search(j, s, re.IGNORECASE):
            return None

    # remove crime, accidents, negative news
    bad_topics = [
        "murder", "shot", "dead", "killed", "rape", "assault", "kidnap",
        "battery", "arrest", "police", "violence", "crime",
        "court", "jail", "charges", "scam", "fraud",
        "minister", "election", "bjp", "congress", "trump"
    ]
    for b in bad_topics:
        if b in s.lower():
            return None

    # clean whitespace
    s = re.sub(r"\s+", " ", s)

    return s


def clean_text(text):
    # split by . ? !
    raw = re.split(r"[.!?]", text)
    clean = []

    seen = set()
    for s in raw:
        s = clean_sentence(s)
        if s and s not in seen:
            seen.add(s)
            clean.append(s)

    return clean


# -----------------------------
# Load model ON GPU 🔥
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# -----------------------------
# Load dataset
# -----------------------------
with open("dataset.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# -----------------------------
# CLEAN the dataset 🧼
# -----------------------------
print("🧹 Cleaning text...")
chunks = clean_text(text)

print(f"Total clean chunks: {len(chunks)}")

# -----------------------------
# Compute Embeddings (GPU)
# -----------------------------
all_embeddings = []
batch_size = 2048  # good for GTX 1650

print("🔥 Computing embeddings...")
for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding"):
    batch = chunks[i:i+batch_size]
    emb = model.encode(batch, convert_to_numpy=True)
    all_embeddings.append(emb)

embeddings = np.vstack(all_embeddings).astype("float32")
print("Embeddings shape:", embeddings.shape)

# -----------------------------
# Build FAISS Index
# -----------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# -----------------------------
# Save DB
# -----------------------------
faiss.write_index(index, "faiss_index.bin")
pickle.dump(chunks, open("chunks.pkl", "wb"))

print("\n🔥 FAISS Vector DB created successfully with CLEANED dataset + GPU!")
