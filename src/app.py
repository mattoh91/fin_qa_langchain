from io import BytesIO

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader
import streamlit as st


def get_pdf_text(pdf_docs: list[BytesIO]) -> str:
    """Extracts string from streamlit UploadedFile

    Args:
        pdf_docs (list[BytesIO]): List containing multiple streamlit UploadedFiles

    Returns:
        str: Text data
    """

    text_data = ""

    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text_data += (page.extract_text())

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

def main():
    # Load OpenAI and HuggingFaceHub API keys
    load_dotenv()

    st.set_page_config(page_title="Financial Statement Chatbot", page_icon=":robot_face:")

    st.title("Financial Statement Chatbot :robot_face:")
    st.text_input("Ask me about your financial statements!", "Type query here ...")

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

if __name__ == '__main__':
    main()