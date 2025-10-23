import requests
from bs4 import BeautifulSoup
import csv
import json
import os

def run(params={}, timestamp="default"):
    # Merge defaults and user params
    from pathlib import Path
    import json as js
    with open("config/config.json") as f:
        config = js.load(f)["scraper"]

    url = params.get("url", config["url"])
    output_format = params.get("output_format", config["output_format"])
    max_items = params.get("max_items", config["max_items"])

    # Make request
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Example: scraping titles and links from Hacker News
    items = []
    for row in soup.select(".athing")[:max_items]:
        title = row.select_one(".titleline a").text
        link = row.select_one(".titleline a")["href"]
        items.append({"title": title, "link": link})

    # Save output
    output_dir = Path(f"outputs/scraper/{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_format == "csv":
        keys = items[0].keys()
        with open(output_dir / "data.csv", "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(items)
    else:
        with open(output_dir / "data.json", "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)

    return {"count": len(items), "output": str(output_dir)}