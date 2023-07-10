# fin_qa_langchain

# Repo Structure
```
.
├── assets
│   └── images
├── conf
│   └── base
├── data
├── docker
├── notebooks
└── src
    └── __pycache__
```

# Limitations
* DocLoader: Langchain's API for PyPDF did not allow using Streamlit's UploadedFile directly.
* Memory: Could not use `ConversationSummaryMemory` as it does not save separate Human and AI messages.
* Models: Ran into OOM issues when trying to use open-sourced embedding model (Instructor) and LLM (Falcon).

# To Do
1. Return source docs > need to figure out how to output source docs
2. Tab data store > Unnecessary so far but can consider FAISS merge with existing store
3. Chain of thought / react / combat hallucinations