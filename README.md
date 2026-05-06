# 📃 Invoice Details Extractor

An AI-powered invoice analysis chatbot that extracts and answers questions from invoice images and PDF documents using Groq AI.

---

## 🚀 Live Demo

👉 [ai-invoice-details-extractor.streamlit.app](https://ai-invoice-details-extractor.streamlit.app)

---

## 📌 Features

- 📄 **PDF Support** — Upload PDF invoices and extract text for analysis
- 🖼️ **Image Support** — Upload JPG/PNG invoice images for analysis
- 💬 **Conversational Chatbot** — Ask follow-up questions and cross-question the AI about your invoice
- 🧠 **Context Memory** — Full chat history maintained throughout the session
- 🌐 **Multilingual** — Responds in the same language as your question
- ⚡ **Powered by Groq** — Fast and free AI backend for both images and PDFs

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web application framework |
| [Groq - LLaMA 4 Scout](https://groq.com) | Image invoice analysis (Vision) |
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

### 3. Set Up API Key

Create a `.streamlit/secrets.toml` file:
```toml
GROQ_API_KEY = "your_groq_api_key"
```

Or create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key
```

> **Get your Groq API Key (Free)** → [console.groq.com](https://console.groq.com)

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `GROQ_API_KEY` | Groq API Key | [Groq Console](https://console.groq.com) |

---

## 📖 How It Works

```
Upload Invoice (PDF or Image)
        ↓
   PDF? → Extract text with PyPDF → Send to Groq LLaMA 3.3 70B
        ↓
  Image? → Convert to base64 → Send to Groq LLaMA 4 Scout (Vision)
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
python-dotenv
pypdf
groq
```

---

## 🖥️ Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `GROQ_API_KEY` in **Settings → Secrets**
5. Deploy!

---

## 🙋‍♀️ Author

**Piya** — BCA Student, Avantika University, Ujjain

[![GitHub](https://img.shields.io/badge/GitHub-piya--b31-black?logo=github)](https://github.com/piya-b31)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
