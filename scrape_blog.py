import requests
from bs4 import BeautifulSoup
from newspaper import Article
import os, re, time, random
from concurrent.futures import ThreadPoolExecutor, as_completed

os.makedirs("data", exist_ok=True)

# --- Real Browser Headers (Avoid Blocks) ---
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0 Safari/537.36"
    )
}

# --- Your URLs ---
urls = [
    # --- Machine Learning Blogs ---
    "https://www.geeksforgeeks.org/machine-learning/",
    "https://www.geeksforgeeks.org/artificial-intelligence/",
    "https://machinelearningmastery.com/",
    "https://www.kdnuggets.com/",
    "https://www.analyticsvidhya.com/blog/",
    "https://towardsdatascience.com/",
    "https://theaisummer.com/",
    "https://lilianweng.github.io/",
    "https://ai.googleblog.com/",
    "https://openai.com/blog",
    "https://ai.facebook.com/blog/",
    "https://deepmind.google/discover/blog/",
    "https://www.marktechpost.com/category/machine-learning/",
    "https://www.ml6.eu/blog",
    "https://databricks.com/blog",
    "https://blog.roboflow.com/",

    # --- Data Science ---
    "https://www.datacamp.com/blog",
    "https://www.kaggle.com/discussion",
    "https://www.kdnuggets.com/category/data-science",
    "https://www.analyticsvidhya.com/category/data-science/",
    "https://r4ds.hadley.nz/",
    "https://realpython.com/",
    "https://pythonprogramming.net/",
    "https://docs.python.org/3/tutorial/",

    # --- AI NEWS ---
    "https://venturebeat.com/category/ai/",
    "https://thenextweb.com/news/",
    "https://www.zdnet.com/topic/artificial-intelligence/",
    "https://www.theverge.com/ai-artificial-intelligence",
    "https://techcrunch.com/tag/artificial-intelligence/",

    # --- General Tech ---
    "https://www.wired.com",
    "https://www.arstechnica.com",
    "https://gizmodo.com/",
    "https://developer.android.com/news",
    "https://developer.apple.com/news/",
    "https://cloud.google.com/blog",
    "https://aws.amazon.com/blogs/",
    "https://azure.microsoft.com/en-us/blog/",

    # --- Security ---
    "https://krebsonsecurity.com/",
    "https://thehackernews.com/",
    "https://portswigger.net/daily-swig",
    "https://www.cybersecurity-insiders.com/",

    # --- Web Development ---
    "https://developer.mozilla.org/en-US/docs/Web",
    "https://www.freecodecamp.org/news/",
    "https://www.w3schools.com/",
    "https://css-tricks.com/",
    "https://web.dev/",
    "https://javascript.plainenglish.io/",

    # --- Programming Tutorials ---
    "https://www.javatpoint.com",
    "https://www.tutorialspoint.com",
    "https://cplusplus.com/",
    "https://www.learncpp.com/",
    "https://www.programiz.com/python-programming",
    "https://www.scaler.com/topics/",
    "https://www.studytonight.com",

    # --- Universities (High-Quality ML Material) ---
    "https://ai.stanford.edu/blog/",
    "https://bair.berkeley.edu/blog/",
    "https://cs.stanford.edu/news/",
    "https://mitnews.mit.edu/topic/artificial-intelligence2",
    "https://news.mit.edu/topic/computer-science",
    "https://news.mit.edu/topic/machine-learning",

    # --- Official Docs (Super Clean Text) ---
    "https://pytorch.org/blog/",
    "https://www.tensorflow.org/blog",
    "https://numpy.org/doc/stable/",
    "https://pandas.pydata.org/docs/",
    "https://scikit-learn.org/stable/whats_new.html",

    # --- Indian Tech Blogs ---
    "https://www.indiatoday.in/technology",
    "https://www.gadgets360.com/news",
    "https://www.livemint.com/technology",
    "https://www.moneycontrol.com/news/technology/",
]

# ---------------------------
# Extract all article URLs from a page
# ---------------------------
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_links(url):
    try:
        print(f"🔎 Extracting links from {url}")

        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            print("❌ Failed:", response.status_code)
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])  # handle relative URLs

            if len(href) > 25:
                if any(x in href.lower() for x in ["news", "blog", "article", "story", "post"]):
                    links.add(href)

        return list(links)

    except Exception as e:
        print("⚠ Link extraction error:", url, "→", e)
        return []


# ---------------------------
# Scrape a single article
# ---------------------------
def scrape_article(url):
    try:
        article = Article(url)

        article.download()
        article.parse()

        text = article.text.strip()

        if len(text) < 300:
            return None

        safe_name = re.sub(r"\W+", "_", url)[:80] + ".txt"

        with open(os.path.join("data", safe_name), "w", encoding="utf-8") as f:
            f.write(text)

        return f"✔ Article saved: {safe_name}"

    except:
        return None


# ---------------------------
# Scrape full website
# ---------------------------
def scrape_site(url):
    links = extract_links(url)

    print(f"📄 Found {len(links)} article links on {url}")

    saved = 0

    for link in links:
        result = scrape_article(link)
        if result:
            saved += 1

        time.sleep(random.uniform(0.05, 0.15))  # avoid banning

    return f"➡ {url} → Saved {saved} articles"


# ---------------------------
# MULTI-THREAD LAUNCHER
# ---------------------------
print("🚀 Starting high-speed multi-thread scraping...\n")

with ThreadPoolExecutor(max_workers=25) as executor:
    futures = [executor.submit(scrape_site, url) for url in urls]

    for f in as_completed(futures):
        print(f.result())

print("\n🎉 Scraping Completed Successfully!")
