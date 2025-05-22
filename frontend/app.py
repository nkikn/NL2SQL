import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use BACKEND_URL from .env
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="NL to SQL Chat", page_icon="🧠")
st.title("🧠 Natural Language to SQL Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input field
prompt = st.chat_input("Ask a database question...")
schema = "Table users(id, name, email, age)"

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Make API call to FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Generating SQL..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/query",
                    json={"db_schema": schema, "question": prompt},
                    timeout=1000
                )
                response.raise_for_status()

                data = response.json()
                results = data.get("result", [])

                if not results:
                    message = "❗ No results returned."
                else:
                    # Extract just values from each result
                    flat_results = []
                    for row in results:
                        values = list(row.values())
                        if len(values) == 1:
                            flat_results.append(str(values[0]))
                        else:
                            flat_results.append(" - ".join(str(v) for v in values))

                    # Join into a single string
                    message = ", ".join(flat_results)

            except Exception as e:
                message = f"❌ Error: {str(e)}"

            st.markdown(message)
            st.session_state.messages.append({"role": "assistant", "content": message})
