import requests
from bs4 import BeautifulSoup
from newspaper import Article
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

save_dir = "data"
os.makedirs(save_dir, exist_ok=True)

# ---------------------------
#  REAL HUMAN HEADERS
# ---------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

urls = [
    "https://www.tomshardware.com/news",
    "https://www.sciencealert.com",
    "https://www.livescience.com",
    "https://www.scientificamerican.com",
    "https://www.bbc.com/news/science_and_environment",
    "https://www.bbc.com/news/world",
    "https://edition.cnn.com/world",
    "https://www.aljazeera.com/news/",
    "https://www.reuters.com/world/",
    "https://www.cnbc.com/world/?region=world",
    "https://www.businessinsider.com",
    "https://www.bloomberg.com",
    "https://economictimes.indiatimes.com/news/international",
    "https://timesofindia.indiatimes.com",
    "https://www.hindustantimes.com",
    "https://indianexpress.com",
    "https://www.ndtv.com",
    "https://www.indiatoday.in",
    "https://www.webmd.com/news",
    "https://www.healthline.com/health-news",
    "https://www.medicalnewstoday.com",
    "https://www.analyticsvidhya.com/blog/",
    "https://www.kdnuggets.com/category/news",
    "https://venturebeat.com/category/ai/",
    "https://www.marktechpost.com",
    "https://thenextweb.com",
    "https://www.thehindu.com/education",
    "https://www.indiatoday.in/education-today",
    "https://www.shiksha.com/news",
    "https://www.bbc.com/news/science-environment-56837908",
    "https://www.nationalgeographic.com/environment",
]


# ---------------------------------------
# Extract article links from a webpage
# ---------------------------------------
def extract_links(url):
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        links = set()

        # find all valid hyperlinks
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") and len(href) > 20 and "/news" in href:
                links.add(href)

        return list(links)

    except Exception:
        return []


# ---------------------------------------
# Scrape a single article
# ---------------------------------------
def scrape_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        if len(article.text) < 300:
            return None

        safe_name = re.sub(r"\W+", "_", url)[:60] + ".txt"
        with open(os.path.join(save_dir, safe_name), "w", encoding="utf-8") as f:
            f.write(article.text)

        return safe_name

    except:
        return None


# ---------------------------------------
# Scrape a news site
# ---------------------------------------
def scrape_site(url):
    print(f"\n🔎 Scanning site: {url}")

    # Step 1 — Extract article links
    links = extract_links(url)
    print(f"Found {len(links)} links at {url}")

    saved = 0

    # Step 2 — Scrape article text
    for link in links:
        result = scrape_article(link)
        if result:
            saved += 1

        # Slow down slightly to avoid bans
        time.sleep(random.uniform(0.1, 0.25))

    return f"✔ {url}: Saved {saved} articles"


# ---------------------------------------
# Multi-threaded Execution (FAST)
# ---------------------------------------
print("🚀 Starting SAFE + FAST news scraping...\n")

with ThreadPoolExecutor(max_workers=30) as executor:
    futures = [executor.submit(scrape_site, url) for url in urls]

    for future in as_completed(futures):
        print(future.result())

print("\n🎉 Scraping complete!")
