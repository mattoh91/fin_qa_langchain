import base64
import json
from io import BytesIO

import requests
import streamlit as st
from htmlTemplates import bot_template, css, reference_template, user_template
from PIL import Image


def image_to_base64(img_path: str) -> str:
    img = Image.open(img_path)
    with BytesIO() as buffer:
        img.save(buffer, "png")
        return base64.b64encode(buffer.getvalue()).decode()


def handle_userinput(answer: dict) -> None:
    """Extract llm response and write it into streamlit app using html
    templates.

    Args:
        answer (str): list of strings containing user input question and bot response.
    """

    for i, message in enumerate(answer["chat_history"]):
        # User response is always an even-indexed message
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message).replace(
                    "{{IMG}}", image_to_base64("./assets/images/qmark.png")
                ),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message).replace(
                    "{{IMG}}", image_to_base64("./assets/images/robot.png")
                ),
                unsafe_allow_html=True,
            )
            with st.expander("Sources"):
                st.write(answer["source_documents"])


def main():
    st.set_page_config(
        page_title="Financial Statement Chatbot", page_icon=":robot_face:"
    )
    st.write(css, unsafe_allow_html=True)
    st.title("Financial Statement Chatbot :robot_face:")

    user_question = st.text_input("Ask question about your financial statements:")

    with st.sidebar:
        st.header("Langchain configurations")
        openai_api_key = st.text_input("OpenAI API key")

        temperature = st.slider(
            label=":thermometer: Temperature (creativity level in bot's response)",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
        )

        st.header("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your financial statements here",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if st.button("Upload"):

            if not openai_api_key.startswith("sk-"):
                st.warning("Please enter your OpenAI API key!", icon="⚠")

            with st.spinner("Processing..."):
                pdf_docs = [("files", pdf.getvalue()) for pdf in pdf_docs]
                headers = {"OpenAI-API-Key": openai_api_key}
                requests.post(
                    "http://backend:8080/upload", files=pdf_docs, headers=headers
                )

        st.write(reference_template, unsafe_allow_html=True)

    if user_question:
        if not openai_api_key.startswith("sk-"):
            st.error("Please input your OpenAI API Key!")
        elif pdf_docs is None:
            st.error("Please upload your financial statement pdf first!")
        else:
            payload = {"question": user_question, "temperature": temperature}
            json_payload = json.dumps(payload)
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                "http://backend:8080/chat", data=json_payload, headers=headers
            )
            handle_userinput(response.json())


if __name__ == "__main__":
    main()
