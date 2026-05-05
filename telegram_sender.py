from dotenv import load_dotenv
import os
import requests

load_dotenv()

def send_telegram(docx_path):
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not TOKEN or not CHAT_ID:
        print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")
        return

    # Step 1: Send message
    msg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg_data = {
        "chat_id": CHAT_ID,
        "text": "📡 ResearchRadar: Your weekly AI digest is ready!"
    }

    msg_response = requests.post(msg_url, data=msg_data)
    print("Message:", msg_response.json())

    # Step 2: Send DOCX file
    doc_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

    try:
        with open(docx_path, "rb") as f:
            doc_response = requests.post(
                doc_url,
                data={"chat_id": CHAT_ID},
                files={"document": f}
            )
        print("Document:", doc_response.json())

    except Exception as e:
        print("❌ Error sending document:", e)


# Test directly
if __name__ == "__main__":
    send_telegram("ResearchRadar_20260505.docx")