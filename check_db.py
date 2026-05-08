import streamlit as st
import faiss
import numpy as np
import pickle

st.set_page_config(page_title="FAISS DB Inspector", layout="wide")

st.title("📦 FAISS Vector Database Inspector")

# -------------------------
# LOAD INDEX + CHUNKS
# -------------------------
try:
    index = faiss.read_index("faiss_index.bin")
    chunks = pickle.load(open("chunks.pkl", "rb"))
    st.success("✅ FAISS index and chunks loaded successfully!")
except:
    st.error("❌ Could not load FAISS DB. Make sure build_db_faiss.py was run.")
    st.stop()

# -------------------------
# DB STATS
# -------------------------
num_vectors = index.ntotal
embedding_dim = index.d

st.subheader("📊 Database Information")
st.write(f"**Total vectors (chunks):** {num_vectors}")
st.write(f"**Embedding dimension:** {embedding_dim}")
st.write(f"**Total text chunks loaded:** {len(chunks)}")

# -------------------------
# SHOW SAMPLE CHUNKS
# -------------------------
st.subheader("📘 Sample Chunks From Database")

num_show = st.slider("How many chunks to display?", 1, 20, 5)

for i in range(num_show):
    st.markdown(f"### Chunk {i + 1}")
    st.write(chunks[i])
    st.write("---")

# -------------------------
# SEARCH TESTING
# -------------------------
st.subheader("🔍 Test a Search Query")

query = st.text_input("Type something to test vector search:")

if query:
    # Need correct shape for FAISS search
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embed = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embed, 3)

    st.write("### 🧠 Top 3 Results From DB:")

    for rank, idx in enumerate(indices[0]):
        st.markdown(f"#### Rank {rank + 1} — Chunk ID {idx}")
        st.write(chunks[idx])
        st.write(f"**Distance:** {distances[0][rank]}")
        st.write("---")
