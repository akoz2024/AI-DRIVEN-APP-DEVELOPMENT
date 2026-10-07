import os
from pathlib import Path

import httpx
import streamlit as st
from dotenv import load_dotenv
from google.genai import errors as genai_errors
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"


def get_api_key():
    """Return the Gemini API key from .env, or stop the app if it's missing."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        st.error(
            "**GEMINI_API_KEY not found.** Add a line like `GEMINI_API_KEY=your-key` to the "
            f"`.env` file in `{Path(__file__).parent}`, then restart the app."
        )
        st.stop()
    return api_key


def check_data_dir():
    """Stop the app unless DATA_DIR is a folder with at least one visible file."""
    if not DATA_DIR.is_dir():
        st.error(
            f"**Data folder not found.** The app expected a folder at `{DATA_DIR}`. "
            "Create it and put the student handbook PDF inside, then restart the app."
        )
        st.stop()

    # Ignore hidden files like .DS_Store; SimpleDirectoryReader skips them too.
    files = [f for f in DATA_DIR.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        st.error(
            f"**The data folder is empty.** Add the student handbook PDF to `{DATA_DIR}`, "
            "then restart the app."
        )
        st.stop()


@st.cache_resource(show_spinner="Indexing the handbook...")
def get_query_engine(api_key):
    """Index the documents in DATA_DIR and return a query engine (built once, then cached)."""
    Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Babson Handbook Chatbot")

# Fail fast: the app can't do anything without a key and documents.
api_key = get_api_key()
check_data_dir()

try:
    query_engine = get_query_engine(api_key)
except genai_errors.ClientError as e:
    st.error(
        "**Gemini rejected the API key.** Check that `GEMINI_API_KEY` in `.env` is a valid key "
        f"from https://aistudio.google.com/apikey, then restart the app.\n\nDetails: {e}"
    )
    st.stop()
except (OSError, ValueError) as e:
    st.error(
        f"**Couldn't build the search index.** Check that the files in `{DATA_DIR}` open "
        "correctly and that you're online (the embedding model downloads on first run), "
        f"then restart the app.\n\nDetails: {e}"
    )
    st.stop()
except Exception as e:
    st.error(f"**Unexpected error while starting the chatbot.** Details: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask a question about the student handbook...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Fallback: one failed question shouldn't take down the app.
    try:
        with st.spinner("Searching..."):
            response = query_engine.query(prompt)
    except genai_errors.ClientError as e:
        if e.code == 429:
            st.error("**Gemini's rate limit was hit.** Wait a minute and ask again.")
        else:
            st.error(f"**Gemini couldn't answer that question.** Try rephrasing it.\n\nDetails: {e}")
    except genai_errors.ServerError:
        st.error("**Gemini is having trouble right now.** Try your question again in a moment.")
    except httpx.TransportError:
        st.error("**Couldn't reach Gemini.** Check your internet connection and ask again.")
    except Exception as e:
        st.error(f"**Something went wrong answering that question.** Try again.\n\nDetails: {e}")
    else:
        answer = response.response
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
