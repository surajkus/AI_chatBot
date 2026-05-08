import os
from concurrent.futures import ThreadPoolExecutor, as_completed

data_dir = "data"
output_file = "dataset.txt"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return ""

files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".txt")]

print(f"🚀 Found {len(files)} files. Starting merge using 80 threads...")

with ThreadPoolExecutor(max_workers=80) as executor:
    futures = {executor.submit(read_file, file): file for file in files}

with open(output_file, "w", encoding="utf-8") as out:
    for fut in as_completed(futures):
        text = fut.result()
        if text:
            out.write(text + "\n\n")

print("✔ Ultra-fast merge completed!")
