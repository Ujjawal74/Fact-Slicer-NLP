from flask import Flask, render_template, request, jsonify
import spacy
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Filters
"""
KEYWORDS = ["yojana", "scheme", "laid", "foundation", "disbursed", "loan",  
            "crore", "cr", "lakh", "lakhs", "registered", "capacity", "inaugurated",
            "plant", "km", "mw", "installed", "bypass", "approved", "announced"]
"""

"""
✅ Key spaCy Entity Labels for Current Affairs Extraction

Entity Label     | What It Catches                                 | Example Matches
-----------------|--------------------------------------------------|------------------------------------------------------------
CARDINAL         | Any numeric value (count or general number)      | 800, 33 lakh, 1070, 500
QUANTITY         | Numeric + unit of measurement                    | 14.4 km, 800 MW, 2600 metric tonnes, 2 lakh tonnes
MONEY            | Monetary amounts with currency symbols or terms  | ₹1,070 crore, ₹33 lakh crore, 130 crore, Rs 6500 crore
PERCENT          | Percentage values                                | 10%, 66%, 100 percent
ORDINAL          | Positional indicators                            | 1st, 10th, second, fifth
DATE             | Explicit date expressions                        | 14 April 2025, past decade, 2023, next year
TIME             | Time indicators (optional, rarely used)          | 3:00 PM, this morning
GPE              | Country, city, state names                       | India, Haryana, Yamunanagar, Delhi
ORG              | Organizations and institutions                   | Government of India, PMO, NITI Aayog, RBI, Bharatmala
FAC              | Infrastructure like plants, airports, roads      | Deenbandhu Thermal Plant, Rewari Bypass, AIIMS
EVENT            | Named historical or scheduled events             | Jallianwala Bagh Massacre, Budget 2024, G20 Summit
LAW              | Official schemes or acts (sometimes detected)    | Fasal Bima Yojana, GST, PM-Kisan
PRODUCT          | Infrastructure/products (contextual triggers)    | solar panel, compressed biogas plant, thermal unit
"""

KEYWORDS = ["yojana", "signs", "sign", "MoU", "approved", "announced", "launched", "passed"]
IMPORTANT_LABELS = {"CARDINAL", "QUANTITY", "MONEY"}
REMOVE_KEYWORDS = ["Posted On:", "Release ID:", "pib.gov.in", "MJPS/SR"]

def has_keyword(sent):
    return any(re.search(rf'\b{re.escape(kw)}\b', sent.lower()) for kw in KEYWORDS)

def get_matched_keywords(sent):
    return [kw for kw in KEYWORDS if re.search(rf'\b{re.escape(kw)}\b', sent.lower())]

def get_numeric_entities(doc_sent):
    return [
        ent.text for ent in doc_sent.ents
        if ent.label_ in IMPORTANT_LABELS and any(c.isdigit() for c in ent.text)
    ]

def extract_sentences(text):
    # Step 1: Clean each line and remove unwanted
    lines = [
        line.strip() for line in text.splitlines()
        if line.strip() and not any(rem in line for rem in REMOVE_KEYWORDS)
    ]

    # Step 2: Run spaCy on each line individually to preserve structure
    sentences = []
    for line in lines:
        doc = nlp(line)
        sentences.extend([sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 40])

    # Step 3: Filter out any sentence with remove keywords
    filtered_sentences = [s for s in sentences if not any(rem in s for rem in REMOVE_KEYWORDS)]

    # Step 4: Match on keywords or entity presence
    results = []
    for sent in filtered_sentences:
        doc_sent = nlp(sent)
        entities = get_numeric_entities(doc_sent)
        keywords = get_matched_keywords(sent)
        if entities or keywords:
            results.append((sent, {"entities": entities, "keywords": keywords}))
    return results

def fetch_text_from_url(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Get Title
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()
        elif soup.title and soup.title.string:
            title = soup.title.string.strip()
        else:
            title = url

        # Extract content with line breaks preserved
        content = ""
        for tag in ['article', 'main', 'div']:
            section = soup.find(tag)
            if section:
                content = section.get_text(separator="\n")  # 🔥 Keep line breaks
                break
        if not content:
            content = soup.get_text(separator="\n")

        return title, content
    except Exception as e:
        return url, f"Error: {str(e)}"  # 🔁 Send error to frontend

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    urls = request.json.get("urls", [])
    result_blocks = []
    for url in urls:
        title, content = fetch_text_from_url(url.strip())
        if content.startswith("Error:"):
            result_blocks.append({
                "title": title,
                "lines": [[content, {"entities": [], "keywords": []}]]
            })
        else:
            lines = extract_sentences(content)
            result_blocks.append({
                "title": title,
                "lines": lines
            })
    return jsonify(result_blocks)

if __name__ == "__main__":
    app.run(debug=True)
