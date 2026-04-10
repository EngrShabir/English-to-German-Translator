# English-to-German-Translator
English→German translator using Gemini AI API + SQLite. Translate, save, read and delete translations.
# 🌍 English → German Text Translator

A command-line Python app that translates English text to German using the **Gemini AI API**, with a built-in **SQLite database** to save, read, and manage your translations.

Built as part of my Python portfolio while preparing for my **Digital Engineering program at Bauhaus University Weimar, Germany**.

---

## ✨ Features

- 🔤 Translate English text to German using Google Gemini AI
- 💾 Save translations with a custom title and timestamp
- 📋 View all saved translations in a clean table
- 📖 Read English only, German only, or both side by side
- 🗑️ Delete saved translations
- 📝 Multi-line text input support

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Google Gemini API (`google-genai`) | AI translation |
| SQLite3 | Local database storage |
| `datetime` | Timestamps |
| `os` | Secure API key loading from environment |

---

## 📁 Project Structure

```
english-german-translator/
│
├── main.py        # Main application
├── texts.db       # SQLite database (auto-created on first run)
├── .env           # Your API key (not uploaded to GitHub)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/english-german-translator.git
cd english-german-translator
```

### 2. Install dependencies
```bash
pip install google-genai
```

### 3. Set your Gemini API key

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

### 4. Run the app
```bash
python main.py
```

---

## 🖥️ How to Use

```
=============================================
  🌍 English → German Text Translator
=============================================

What do you want to do?
  [1] Translate & save a new text
  [2] View saved texts
  [q] Quit
```

1. Choose **[1]** to translate — paste your English text, type `END` when done
2. Preview the German translation, then choose to save it or not
3. Choose **[2]** to browse all saved translations
4. Open any translation by ID to read or delete it

---

## 🔑 API Info

- Uses **Gemini 2.5 Flash Lite** model
- Free tier: ~1000 requests/day
- API key is loaded securely from environment variable — never hardcoded

---

 
---

## 📜 License

MIT License — free to use and modify
