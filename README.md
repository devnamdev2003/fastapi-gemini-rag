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



**Core Project Structure**

* `app/main.py`: Initializes the FastAPI application and exposes the `/ask` endpoint.


* `app/rag.py`: Handles context retrieval and prompts the `gemini-3.5-flash-lite` model for answers.


* `app/retriever.py`: Executes hybrid similarity searches against the local vector database.


* `app/embedding.py`: Connects to the `gemini-embedding-2` model to vectorize text.


* `app/chunker.py`: Splits large documents into manageable text blocks.


* `app/vector_store.py`: Builds and saves the `vector_store.json` file.


* `test_api.py`: A utility script to verify your Gemini API key connection.

---

## More Learning:

- [About](./notes/about.md)
- [Work-Flow](./notes/work-flow.md)
- [Deployment on vercel](./notes/deployment.md)
- [Vector](./notes/vector.md)
