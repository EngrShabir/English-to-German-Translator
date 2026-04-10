import os
import sqlite3
import datetime
from google import genai

# ── CONFIG ──────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_FILE = "texts.db"
# ────────────────────────────────────────────────────────

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Set it before running the app.")

client = genai.Client(api_key=GEMINI_API_KEY)

# ── DATABASE SETUP ───────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            english_text TEXT NOT NULL,
            german_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_text(title, english_text, german_text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('''
        INSERT INTO texts (title, english_text, german_text, created_at)
        VALUES (?, ?, ?, ?)
    ''', (title, english_text, german_text, created_at))
    conn.commit()
    conn.close()
    print("✅ Text saved successfully!")

def list_texts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, created_at FROM texts ORDER BY created_at DESC')
    texts = cursor.fetchall()
    conn.close()
    return texts

def get_text(text_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM texts WHERE id = ?', (text_id,))
    text = cursor.fetchone()
    conn.close()
    return text

def delete_text(text_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM texts WHERE id = ?', (text_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("❌ No text found with that ID.")
    else:
        print("🗑️  Text deleted.")
    conn.close()

# ── GEMINI ───────────────────────────────────────────────
def translate_to_german(text):
    print("\n⏳ Translating... please wait.")
    prompt = f"Translate the following English text to German. Return ONLY the German translation, nothing else:\n\n{text}"
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text.strip()

# ── MENU ACTIONS ─────────────────────────────────────────
def translate_and_save():
    print("\n" + "─" * 45)
    title = input("📝 Enter a title for this text: ").strip()
    if not title:
        print("❌ Title cannot be empty.")
        return

    print("📄 Paste your English text below.")
    print("   (When done, type END on a new line and press Enter)")
    print("─" * 45)

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    english_text = "\n".join(lines).strip()
    if not english_text:
        print("❌ No text entered.")
        return

    german_text = translate_to_german(english_text)
    print("\n✅ Translation done!\n")
    print("─" * 45)
    if len(german_text) > 500:
        preview = german_text[:500]
        last_space = preview.rfind(' ')
        if last_space > 0:
            preview = preview[:last_space]
        print(preview + "...")
    else:
        print(german_text)
    print("─" * 45)

    save = input("\n💾 Save this text? (y/n): ").strip().lower()
    if save == "y":
        save_text(title, english_text, german_text)

def view_texts():
    texts = list_texts()
    if not texts:
        print("\n📭 No texts saved yet.")
        return

    print("\n" + "─" * 45)
    print(f"  {'ID':<5} {'TITLE':<25} {'DATE'}")
    print("─" * 45)
    for t in texts:
        print(f"  {t[0]:<5} {t[1]:<25} {t[2]}")
    print("─" * 45)

    choice = input("\nEnter text ID to read it (or press Enter to go back): ").strip()
    if choice.isdigit():
        read_text(int(choice))

def read_text(text_id):
    text = get_text(text_id)
    if not text:
        print("❌ Text not found.")
        return

    print("\n" + "=" * 45)
    print(f"  📄 {text[1]}")
    print(f"  🕐 {text[4]}")
    print("=" * 45)

    view = input("\nView: [1] English  [2] German  [3] Both: ").strip()

    if view == "1":
        print("\n🇬🇧 ENGLISH:\n")
        print(text[2])
    elif view == "2":
        print("\n🇩🇪 GERMAN:\n")
        print(text[3])
    elif view == "3":
        print("\n🇬🇧 ENGLISH:\n")
    else:
        print("❌ Invalid choice.")
        print(text[2])
        print("\n🇩🇪 GERMAN:\n")
        print(text[3])

    print("\n" + "─" * 45)
    delete = input("🗑️  Delete this text? (y/n): ").strip().lower()
    if delete == "y":
        delete_text(text_id)

# ── MAIN ─────────────────────────────────────────────────
def main():
    init_db()
    print("=" * 45)
    print("  🌍 English → German Text Translator")
    print("=" * 45)

    while True:
        print("\nWhat do you want to do?")
        print("  [1] Translate & save a new text")
        print("  [2] View saved texts")
        print("  [q] Quit")
        choice = input("\nYour choice: ").strip().lower()

        if choice == "1":
            translate_and_save()
        elif choice == "2":
            view_texts()
        elif choice == "q":
            print("\nAuf Wiedersehen! 👋")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()