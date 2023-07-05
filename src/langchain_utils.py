from io import BytesIO

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from pypdf import PdfReader

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

    # OpenAI uses text-embedding-ada-002 embedding model by default
    # ada-002 uses cl100k_base tokeniser and takes max 8191 input tokens
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vectorstore

def get_conversation_chain(
    vectorstore: FAISS,
    temperature: float
) -> ConversationalRetrievalChain:
    """Create conversation chain

    Args:
        vectorstore (FAISS): FAISS vectorstore object

    Returns:
        ConversationalRetrievalChain: A conversation retrieval chain object
    """

    llm = ChatOpenAI(temperature=temperature)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain