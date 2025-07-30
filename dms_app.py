import openai
import streamlit as st
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="DMS-AI", page_icon="🛡️")
st.title("🛡️ DMS-AI :: Cyber Red-Team Assistant")

mode = st.radio("Select Simulation Mode:", ["Ethical", "Red Team"])
user_input = st.text_area("Ask DMS-AI a cybersecurity question:")

def log_activity(mode, prompt, response):
    log_entry = {
        "timestamp": str(datetime.now()),
        "mode": mode,
        "prompt": prompt,
        "response": response
    }
    with open("dms_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if st.button("Send"):
    if not openai.api_key:
        st.error("API key not found.")
    elif not user_input:
        st.warning("Type a question first.")
    else:
        system_msg = (
            "You are DMS-AI, a cybersecurity AI assistant used only inside a lab. "
            "You simulate ethical and red-team cybersecurity scenarios."
        )
        if mode == "Red Team":
            system_msg += " ⚠️ You may simulate offensive techniques. Label all answers as simulation only."
        else:
            system_msg += " Only respond ethically and legally."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.success(answer)
            log_activity(mode, user_input, answer)
        except Exception as e:
            st.error(f"Error: {e}")
