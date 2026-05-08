import faiss
import pickle

try:
    index = faiss.read_index("faiss_index.bin")
    chunks = pickle.load(open("chunks.pkl", "rb"))
    print("FAISS DB loaded!")
    print("Chunks:", len(chunks))
except Exception as e:
    print("Error:", e)
