import streamlit as st
from google import genai
from google.genai import types
import pathlib
import os

# Set up Gemini client
genai_client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# Preload the PDF
pdf_path = pathlib.Path("musnad.pdf")  # Change to your actual file name
pdf_bytes = pdf_path.read_bytes()

# Streamlit page setup
st.set_page_config(page_title="Tamil Chat with Gemini", layout="wide")
st.title("📜 Chat with Musnad Ahamed")

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat messages
for q, a in st.session_state.chat:
    with st.chat_message("user"):
        st.markdown(f"**🧑‍💻:** {q}")
    with st.chat_message("assistant"):
        st.markdown(f"**🤖:** {a}")

# User input
user_input = st.chat_input("Ask your questions in English , Tamil or Tanglish")
preprompt = """You are a knowledgeable and respectful Islamic assistant that helps users by answering questions strictly based on the Hadiths from Musnad Ahmad provided in the document. Users may ask their questions in English, Tamil, or Tanglish (Tamil written in English letters). Detect the language of the question and respond in the same language. If the answer cannot be found in the content, reply:
"மன்னிக்கவும், இந்த கேள்விக்கு பதில் இந்த ஆவணத்தில் காணப்படவில்லை." (in Tamil)
or
"Sorry, I couldn't find an answer to this question in the document." *(in English/Tanglish as appropriate).
Be precise, respectful, and avoid guessing or adding anything outside the document. """


# On submit
if user_input:
    #user_input2 = preprompt + user_input
    with st.chat_message("user"):
        st.markdown(f"**🧑‍💻:** {user_input}")

    # Generate response using Gemini with preloaded PDF
    try:
        response = genai_client.models.generate_content(
            model="gemini-1.5-pro",
            config=types.GenerateContentConfig(
                system_instruction=preprompt),
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                user_input
            ]
        )
        answer = response.text

    except Exception as e:
        answer = f"பிழை ஏற்பட்டது: {e}"

    with st.chat_message("assistant"):
        st.markdown(f"**🤖:** {answer}")

    # Save to chat history
    st.session_state.chat.append((user_input, answer))
