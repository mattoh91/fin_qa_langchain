# fin_qa_langchain

# Limitations
* DocLoader: Langchain's API for PyPDF did not allow using Streamlit's UploadedFile directly.
* Memory: Could not use `ConversationSummaryMemory` as it does not save separate Human and AI messages.
* Models: Ran into OOM issues when trying to use open-sourced embedding model (Instructor) and LLM (Falcon).