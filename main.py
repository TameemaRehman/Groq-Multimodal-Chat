import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class ChatSession:
    def __init__(self, model="meta-llama/llama-4-scout-17b-16e-instruct"):
        # guarantee we have a key before anything else
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY not found in environment. Please set it before running.")
        self.model = model
        self.history = [
            {"role": "system", "content": "You are a helpful multimodal assistant."}
        ]

    def send(self, prompt_text, image_url=None):
        # Build the new user message
        if image_url:
            user_content = [
                {"type": "text",    "text": prompt_text},
                {"type": "image_url",    "image_url": {"url": image_url}}
            ]
        else:
            user_content = prompt_text

        # Append to history
        self.history.append({"role": "user", "content": user_content})

        # Prepare payload
        payload = {
            "model": self.model,
            "messages": self.history
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # Call the API
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            return f"HTTP Error: {err}\nDetails: {resp.text}"

        data = resp.json()
        assistant_reply = data["choices"][0]["message"]["content"]

        # Save assistant’s reply into history
        self.history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply


if __name__ == "__main__":
    session = ChatSession()

    while True:
        img = input("\nImage URL (or blank): ").strip() or None
        txt = input("Your prompt: ").strip()
        if txt.lower() in {"exit", "quit"}:
            break

        reply = session.send(txt, img)
        print("\nAssistant:", reply)
