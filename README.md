# 📃 Invoice Details Extractor

An AI-powered invoice analysis chatbot that extracts and answers questions from invoice images and PDF documents using Google Gemini and Groq AI.

---

## 🚀 Live Demo

👉 [ai-invoice-details-extractor.streamlit.app](https://ai-invoice-details-extractor.streamlit.app)

---

## 📌 Features

- 📄 **PDF Support** — Upload PDF invoices and extract text for analysis
- 🖼️ **Image Support** — Upload JPG/PNG invoice images for visual analysis
- 💬 **Conversational Chatbot** — Ask follow-up questions and cross-question the AI about your invoice
- 🧠 **Context Memory** — Full chat history maintained throughout the session
- 🌐 **Multilingual** — Responds in the same language as your question
- ⚡ **Dual AI Backend** — Groq (PDF) + Gemini (Images) for optimal performance

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web application framework |
| [Google Gemini 2.0 Flash](https://ai.google.dev) | Image invoice analysis |
| [Groq - LLaMA 3.3 70B](https://groq.com) | PDF invoice analysis |
| [PyPDF](https://pypdf.readthedocs.io) | PDF text extraction |
| [Pillow](https://pillow.readthedocs.io) | Image processing |
| [Python Dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |

---

## 📂 Project Structure

```
ai-invoice-details-extractor/
├── app.py               # Main application file
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/piya-b31/ai-invoice-details-extractor.git
cd ai-invoice-details-extractor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your_gemini_api_key"
GROQ_API_KEY = "your_groq_api_key"
```

Or create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

> **Get your API keys:**
> - Gemini API Key → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
> - Groq API Key → [console.groq.com](https://console.groq.com)

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API Key | [AI Studio](https://aistudio.google.com/app/apikey) |
| `GROQ_API_KEY` | Groq API Key | [Groq Console](https://console.groq.com) |

---

## 📖 How It Works

```
Upload Invoice (PDF or Image)
        ↓
   PDF? → Extract text with PyPDF → Send to Groq (LLaMA 3.3)
        ↓
  Image? → Send to Google Gemini 2.0 Flash
        ↓
   AI analyzes and responds
        ↓
  Ask follow-up questions with full context memory
```

---

## 💡 Usage

1. Open the app in your browser
2. Upload an invoice (PDF or image format)
3. Type your question in the chat box
4. Ask follow-up questions or request a summary

### Example Queries
- *"Summarise this invoice"*
- *"What is the total amount?"*
- *"What is the tax amount?"*
- *"Who is the vendor?"*
- *"What is the due date?"*

---

## 📦 Requirements

```
streamlit
google-genai
python-dotenv
pypdf
groq
```

---

## ⚠️ Known Limitations

- Live microphone recording is not supported on Streamlit Cloud
- Image analysis depends on Gemini API free tier quota
- For best results, use PDF format invoices

---

## 🙋‍♀️ Author

**Piya** — BCA Student, Avantika University, Ujjain

[![GitHub](https://img.shields.io/badge/GitHub-piya--b31-black?logo=github)](https://github.com/piya-b31)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
