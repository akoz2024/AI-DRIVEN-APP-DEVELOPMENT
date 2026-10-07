# RAG Chatbot — Babson Student Handbook

In-class Activities 10–11 for OIM 3641. A Streamlit chatbot that answers questions about the
Babson undergraduate student handbook using retrieval-augmented generation (RAG): LlamaIndex
indexes the handbook locally with a HuggingFace embedding model, retrieves the most relevant
passages for each question, and sends them to Gemini to write the answer.

## Run it

```bash
cd activities/rag-chatbot
cp .env.example .env          # then paste your key into .env
uv sync
uv run streamlit run app.py
```

`.env` holds `GEMINI_API_KEY` and is git-ignored. `data/` holds the handbook PDF; everything in
that folder gets indexed.

> **Setup note:** the activity's `uv add` list doesn't include `llama-index-readers-file`. Without
> it, `SimpleDirectoryReader` can't parse PDFs and silently indexes the raw PDF bytes as text, so
> every answer is built from garbage. It's added in `pyproject.toml` here.

## Activity 10 write-up

### Test queries

| Question | Handbook chatbot | General chat LLM |
| --- | --- | --- |
| Can I get credit for courses taken somewhere else? | _TODO_ | _TODO_ |
| Are any interest-free loans offered? | _TODO_ | _TODO_ |
| Follow-up: "What if I'm a transfer student?" | _TODO_ | _TODO_ |

### Observations

_TODO after running the app: compare specificity (does it cite Babson's actual policy, e.g. the
Mass No Interest Loan?) versus the general LLM's generic answers._

### Does the chatbot have memory?

Not in the way that matters. LLMs are stateless: every API call starts from nothing. Chat
products like ChatGPT or Claude handle the "memory problem" by resending the conversation so far
with every new message, so the model rereads the whole chat each turn. Once a conversation
outgrows the context window, older turns get dropped or compressed into a summary. Some products
also keep a long-term memory store and retrieve relevant notes into the prompt, which is the same
retrieval idea as RAG, applied to your history instead of a document.

This chatbot keeps the chat in `st.session_state`, but only to **redisplay** it. Each call to
`query_engine.query(prompt)` sends just the newest question, so the model never sees the earlier
turns. A follow-up like "What if I'm a transfer student?" gets retrieved and answered as a
standalone question with no idea what "what if" refers to. Real memory would require passing the
history along, for example with LlamaIndex's chat engine (`index.as_chat_engine()`), which rewrites
follow-ups into standalone questions using the history.

### Screenshots

_TODO_
