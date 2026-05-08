import time
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
texts = ["This is a test sentence."] * 2000

start = time.time()
emb = model.encode(texts, batch_size=512)
end = time.time()

print("Time:", end - start)
