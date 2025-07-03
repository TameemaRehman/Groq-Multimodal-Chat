# app_streamlit.py
import streamlit as st
from main import ChatSession  # your backend logic

# ——— Page config ———
st.set_page_config(page_title="Groq Multimodal Chat", page_icon="🤖")

# ——— Custom heading ———
st.markdown(
    """
    <style>
      /* 1) Import a fun handwritten font */
      @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
      /* 2) Style our heading */
      .custom-heading {
        font-family: 'Pacifico', cursive;
        font-size: 3.5rem;
        color: #222222;
        text-align: center;
        margin: 0.5rem 0 1.5rem;
      }
      /* 3) Tiny shadow to make it pop */
      .custom-heading span {
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
      }
    </style>

    <!-- 4) The heading itself -->
    <h1 class="custom-heading">
      <span>🖼️</span>
      <span style="color:#FF6F61">Groq</span>
      <span style="color:#2E8B57">Multimodal</span>
      <span style="color:#1E90FF">Chat</span>
      <span>💬🚀</span>
    </h1>
    """,
    unsafe_allow_html=True,
)

# Initialize ChatSession once and keep it in session_state
if "chat" not in st.session_state:
    st.session_state.chat = ChatSession()

# ─── Callback for sending and clearing inputs ──────────────────
def on_send():
    """
    This callback runs BEFORE the script reruns.
    Inside here you can mutate session_state safely.
    """
    chat = st.session_state.chat
    prompt = st.session_state.get("prompt", "").strip()
    image_url = st.session_state.get("img_url", "").strip() or None

    # Send to the backend (appends assistant reply into history)
    chat.send(prompt, image_url)

    # Clear the text inputs in session_state (allowed inside callback)
    st.session_state.prompt = ""
    st.session_state.img_url = ""

# ─── 1) Input widgets ─────────────────────────────────────────
# We give each widget a key so we can read/clear it via session_state
prompt = st.text_input(
    label="Your message", 
    placeholder="",    
    key="prompt"
)
img_url = st.text_input(
    label="Image URL (optional)", 
    placeholder="", 
    key="img_url"
)
uploaded_file = st.file_uploader(
    label="…or upload an image", 
    type=["png", "jpg", "jpeg"],
    key="uploaded_file"
)

# CHANGED: Replace form + submit button with a plain button + callback
st.button("Send", on_click=on_send)

# ─── 2) Display the conversation history ───────────────────────
st.markdown("---")
for msg in st.session_state.chat.history:
    if msg["role"] == "system":
        continue

    # choose background & alignment
    if msg["role"] == "user":
        bg    = "#D6F5BF"  # light green
        align = "right"
    else:
        bg    = "#CEE7EF"  # light blue
        align = "left"

    content = msg["content"]
    if isinstance(content, list):
        text = content[0]["text"]
        img  = content[1]["image_url"]["url"]
        html = f"""
        <div style="
            background:{bg};
            padding:8px;
            border-radius:10px;
            margin:4px 0;
            max-width:80%;
            float:{align};
            clear:both;
        ">
          <p style="margin:0;">{text}</p>
          <img src="{img}" width="200"/>
        </div>
        """
    else:
        html = f"""
        <div style="
            background:{bg};
            padding:8px;
            border-radius:10px;
            margin:4px 0;
            max-width:80%;
            float:{align};
            clear:both;
        ">
          <p style="margin:0;">{msg['content']}</p>
        </div>
        """

    st.markdown(html, unsafe_allow_html=True)

# clear floats so widgets below render correctly
st.markdown("<div style='clear:both;'></div>", unsafe_allow_html=True)
