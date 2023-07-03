# Init chat_history and look into weird chat ordering

import base64
from io import BytesIO
from PIL import Image

from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from pypdf import PdfReader
import streamlit as st

from htmlTemplates import (
    css,
    bot_template,
    reference_template,
    user_template
)


def image_to_base64(img_path: str) -> str:
    img = Image.open(img_path)
    with BytesIO() as buffer:
        img.save(buffer, 'png')
        return base64.b64encode(buffer.getvalue()).decode()

def get_pdf_text(pdf_docs: list[BytesIO]) -> str:
    """Extracts string from streamlit UploadedFile

    Args:
        pdf_docs (list[BytesIO]): List containing multiple streamlit UploadedFiles

    Returns:
        str: Text data
    """

    text_data = ""
    for pdf in pdf_docs:
        doc_loader = PdfReader(pdf)
        for page in doc_loader.pages:
            text_data += page.extract_text()

    return text_data

def get_text_chunks(text_data: str) -> list[str]:
    """Split raw text into chunks

    Args:
        text_data (str): Raw text data

    Returns:
        list[str]: List containing chunks of raw text input
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = splitter.split_text(text_data)

    return chunks

def get_vectorstore(chunks: list[str]) -> FAISS:
    """Instantiate Faiss vectorstore

    Args:
        chunks (list[str]): Text chunks

    Returns:
        FAISS: Vectorstore object
    """

    # Uses text-embedding-ada-002 embedding model by default
    # ada-002 uses cl100k_base tokeniser and takes max 8191 input tokens
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vectorstore

def get_conversation_chain(vectorstore: FAISS) -> ConversationalRetrievalChain:
    """Create conversation chain

    Args:
        vectorstore (FAISS): FAISS vectorstore object

    Returns:
        ConversationalRetrievalChain: A conversation retrieval chain object
    """

    llm = ChatOpenAI()
    memory = ConversationBufferWindowMemory(k=4, memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    answer = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = answer["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        # User response is always an even-indexed message
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content)
                .replace("{{IMG}}", image_to_base64("./assets/images/qmark.png")),
                unsafe_allow_html=True
            )
        else:
            st.write(bot_template.replace("{{MSG}}", message.content)
                .replace("{{IMG}}", image_to_base64("./assets/images/robot.png")),
                unsafe_allow_html=True
            )

def main():
    # Load OpenAI and HuggingFaceHub API keys
    load_dotenv()

    st.set_page_config(page_title="Financial Statement Chatbot", page_icon=":robot_face:")
    st.write(css, unsafe_allow_html=True)
    st.title("Financial Statement Chatbot :robot_face:")

    # Instantiate session state "conversation" variable
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    user_question = st.text_input("Ask question about your financial statements:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.header("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your financial statements here",
            type=["pdf"],
            accept_multiple_files=True
        )

        if st.button("Upload"):
            with st.spinner("Processing..."):
                # Get pdf text data
                raw_text = get_pdf_text(pdf_docs)

                # Convert text data into chunks
                chunks = get_text_chunks(raw_text)

                # Create vector store
                vectorstore = get_vectorstore(chunks)

                # Create conversation chain and save it as a stateful variable
                st.session_state.conversation = get_conversation_chain(vectorstore)
        
        st.write(reference_template, unsafe_allow_html=True)


if __name__ == '__main__':
    main()