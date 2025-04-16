# 📰 One-Liner Current Affairs Extractor

This is a Flask + spaCy based web app that extracts exam-relevant one-liner facts from government news articles — perfect for competitive exam preparation like SSC, UPSC, Railways, Banking, etc.

---

## 🔍 Features

- ✅ Paste multiple article URLs (e.g. from [pib.gov.in](https://pib.gov.in))
- ✅ Automatically fetches and processes content
- ✅ Extracts one-liner facts using:
  - Sentence segmentation
  - Keyword filtering
  - Named Entity Recognition (NER)
- ✅ Highlights both:
  - **Entities** → `33 lakh`, `₹410 crore`, `14.4 km`, `2025`
  - **Keywords** → `yojana`, `scheme`, `foundation`, `laid`
- ✅ Modern, responsive Bootstrap 5 interface
- ✅ Progress bar, success/error toasts

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **NLP Engine:** spaCy (`en_core_web_sm`)
- **Scraping:** BeautifulSoup
- **Frontend:** HTML, Bootstrap 5, JavaScript

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/current-affairs-extractor.git
cd current-affairs-extractor
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask app

```bash
python flask_app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

```
.
├── flask_app.py
├── templates/
│   └── index.html
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ✅ Sample Output

```
Title: PM inaugurates development projects in Haryana

1. PM Modi laid the foundation stone of a new terminal at Hisar Airport worth ₹410 crore.
   ➤ Entities: ₹410 crore | Keywords: laid, foundation, crore

2. PM Suryagarh Muft Bijli Yojana can reduce electricity bill to zero.
   ➤ Keywords: yojana
```

---

## ✨ Author

Made with ❤️ by [Ujjawal Biswas](https://krispnotes.in)  
If this helps you, please ⭐ the project and share with others!

---

## 📄 License

This project is free to use and open-source.
