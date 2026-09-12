**Project Overview:**

This application is a FastAPI-based AI assistant that reads company documents, generates vector embeddings using the Google Gemini API, and answers user questions strictly based on the provided context. It utilizes a custom local JSON vector store and implements a hybrid retrieval system combining cosine similarity and keyword matching.

**Prerequisites**

* A Python virtual environment (e.g., `venv/`).


* Required dependencies installed from `requirements.txt`.


* A valid Google Gemini API key.



**Configuration**

* Store your plain-text company policy files (such as `it_support.txt`, `leave_policy.txt`, and `wfh_policy.txt`) inside the `documents/` folder.


* Create a `.env` file in the root directory to safely store your API credentials:


```
GEMINI_API_KEY=your_api_key_here
```



**Usage Instructions**

* **1. Build the Vector Store**: After modifying, adding, or changing a document, you must regenerate the local database. Run the following command from the root directory:


```bash
python -m app.vector_store
```


* **2. Start the API Server**: Launch the FastAPI application:


```bash
uvicorn app.main:app --reload
```


* **3. Test the Application**: Send a POST request to the `/ask` endpoint. You can use the following sample JSON payload:


```json
{
  "question": "How many paid leaves can I carry forward?"
}
```

## More Learning:

- [01-basic-rag](./01-basic-rag/README.md)
- [02-tool-calling](./02-tool-calling/README.md)
