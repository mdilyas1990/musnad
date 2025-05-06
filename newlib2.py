import streamlit as st
from google import genai
from google.genai import types
import pathlib

# Set up Gemini client
genai_client = genai.Client(api_key="AIzaSyBaJInUzY9hvQYVfr2TXUvY5UH7WmzjGsI")

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
preprompt = """whatever question is asked, 
answer from the file if the answer to that 
corresponding questoin is there. If suitable 
answer is not found, just say you cant find the answer for that question. 
Please answer in tamil for all questions . QUESTION : """


# On submit
if user_input:
    user_input2 = preprompt + user_input
    with st.chat_message("user"):
        st.markdown(f"**🧑‍💻:** {user_input}")

    # Generate response using Gemini with preloaded PDF
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                user_input2
            ]
        )
        answer = response.text

    except Exception as e:
        answer = f"பிழை ஏற்பட்டது: {e}"

    with st.chat_message("assistant"):
        st.markdown(f"**🤖:** {answer}")

    # Save to chat history
    st.session_state.chat.append((user_input, answer))
