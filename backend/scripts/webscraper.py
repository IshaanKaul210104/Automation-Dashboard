import requests
from bs4 import BeautifulSoup
import csv
import json
import os

def run(params={}, timestamp="default"):
    from pathlib import Path
    import json as js
    import requests, csv
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    with open("config/config.json") as f:
        config = js.load(f)["scraper"]

    url = params.get("url", config["url"])
    output_format = params.get("output_format", config["output_format"])
    max_items = params.get("max_items", config["max_items"])

    # Fetch and parse HTML
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    items = []

    # 1️⃣ First, look for <article> tags (common for blogs/news)
    for art in soup.find_all("article")[:max_items]:
        link_tag = art.find("a", href=True)
        title_tag = art.find(["h1", "h2", "h3"])
        if link_tag and title_tag:
            title = title_tag.get_text(strip=True)
            link = urljoin(url, link_tag["href"])
            items.append({"title": title, "link": link})

    # 2️⃣ If no <article> tags found, look for heading-based structures
    if not items:
        for heading in soup.find_all(["h1", "h2", "h3"], limit=max_items * 2):
            link_tag = heading.find("a", href=True)
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = urljoin(url, link_tag["href"])
                if title:
                    items.append({"title": title, "link": link})
            if len(items) >= max_items:
                break

    # 3️⃣ If still nothing, fallback to any anchor tags with long text
    if not items:
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if len(text.split()) > 2:  # skip nav links
                link = urljoin(url, a["href"])
                items.append({"title": text, "link": link})
            if len(items) >= max_items:
                break

    # ✅ Save results
    output_dir = Path(f"outputs/scraper/{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    if items:
        if output_format == "csv":
            keys = items[0].keys()
            with open(output_dir / "data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(items)
        else:
            with open(output_dir / "data.json", "w", encoding="utf-8") as f:
                json.dump(items, f, indent=2)
    else:
        with open(output_dir / "data.json", "w", encoding="utf-8") as f:
            json.dump({"error": "No data found"}, f, indent=2)

    return {"count": len(items), "output": str(output_dir)}