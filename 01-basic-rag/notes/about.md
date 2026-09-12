# 🧠 Company Knowledge AI Assistant — What I Have Learned

> **Project:** RAG-based Company Knowledge AI Assistant
> **Goal:** Build an AI system that can answer questions using private/company documents instead of relying only on the LLM's built-in knowledge.

---

## 1. Overall Architecture

The system has two major pipelines.

### A. Document/Knowledge Pipeline

This happens before users ask questions:

```text
Company Documents
       ↓
Document Loading
       ↓
Chunking
       ↓
Embedding
       ↓
Vector Store
```

### B. User Query Pipeline

This happens whenever a user asks a question:

```text
User Question
      ↓
Question Embedding
      ↓
Similarity Search
      ↓
Relevant Chunks
      ↓
Build Context
      ↓
Gemini LLM
      ↓
Answer + Sources
```

---

# 2. LLM — Large Language Model

**LLM = Large Language Model**

Examples:

* Gemini
* GPT
* Claude
* Llama

An LLM can understand and generate natural language.

In this project, Gemini is responsible mainly for **generating the final answer**.

---

# 3. RAG — Retrieval-Augmented Generation

**RAG = Retrieval-Augmented Generation**

Instead of directly asking Gemini:

```text
Question → Gemini → Answer
```

we first retrieve relevant information:

```text
Question
   ↓
Retrieve relevant company information
   ↓
Give information + question to Gemini
   ↓
Answer
```

### RAG has two major parts:

**Retrieval**

Find relevant information.

**Generation**

Gemini generates the final answer using that information.

---

# 4. Knowledge Base

A **knowledge base** is the collection of information available to the AI.

Our project has:

```text
documents/
├── leave_policy.txt
├── wfh_policy.txt
└── it_support.txt
```

These documents form our basic company knowledge base.

---

# 5. Document Loading

`document_loader.py`

Its job is:

```text
File on disk
     ↓
Read file
     ↓
Load text into Python
```

Example:

```text
leave_policy.txt
        ↓
Python
        ↓
{
   filename: "leave_policy.txt",
   content: "Company Leave Policy..."
}
```

---

# 6. Chunking

**Chunking = breaking a large document into smaller pieces.**

Example:

```text
Large Document
      ↓
 ┌───────────┐
 │ Chunk 1   │
 │ Chunk 2   │
 │ Chunk 3   │
 │ Chunk 4   │
 └───────────┘
```

### Why?

We don't want to search or send an entire large document to the LLM every time.

Instead, we want to find only the relevant parts.

### Important terminology

**Chunk** = a small piece of a document.

**Chunk size** = how much text is included in one chunk.

**Chunk overlap** = repeating some text between neighboring chunks so information isn't lost at chunk boundaries.

Our current project uses a simple paragraph-based chunking approach.

---

# 7. Embedding

**Embedding = converting text into a numerical vector that represents the text in the embedding model's semantic space.**

Example:

```text
"Employees can carry forward 10 paid leaves."
                    ↓
             Embedding Model
                    ↓
       [0.12, -0.43, 0.81, ...]
```

Our project uses:

```text
gemini-embedding-2
```

Our current embeddings are 3,072-dimensional by default.

---

# 8. What are those numbers?

The numbers aren't individually:

```text
0.7 = leaves
0.6 = employee
```

Instead, the **whole vector collectively represents the semantic characteristics of the text**.

The embedding model learned language relationships during its training.

Therefore:

```text
"paid leave"
"vacation days"
"carry forward leave"
```

can be represented by vectors that are relatively close in the model's semantic space.

The embedding model doesn't need to see our company documents when processing a user query.

It already learned general language/semantic relationships during training.

---

# 9. Important: Embedding model vs Generation model

These are different jobs.

### Embedding model

```text
Text
 ↓
Vector
```

Our project:

```text
gemini-embedding-2
```

### Generative model

```text
Prompt
 ↓
Text Answer
```

Our project:

```text
gemini-3.5-flash-lite
```

They don't have to be the same model.

For example:

```text
Gemini Embedding
      ↓
Vector Search
      ↓
Relevant Context
      ↓
GPT/Gemini/Claude
      ↓
Answer
```

But the document and query embeddings used for similarity search should normally come from the **same embedding model/compatible embedding space**.

---

# 10. Vector

A **vector** is simply a list of numbers.

Example:

```text
[0.2, 0.5, -0.1, 0.8]
```

Our actual vector is much larger:

```text
[0.021, -0.184, 0.732, ...]
```

with 3,072 dimensions by default in our current setup.

Think of an embedding vector as the text's **semantic coordinates**.

---

# 11. Vector Store

A **vector store** stores:

```text
Document
+
Chunk
+
Embedding
```

Our educational project uses:

```text
vector_store.json
```

Example:

```text
leave_policy.txt
      ↓
Chunk 1
      ↓
[0.12, -0.43, 0.81, ...]
```

In production, we would typically use a proper vector database/search system such as pgvector, Qdrant, Pinecone, Weaviate, Milvus, etc.

---

# 12. Query Embedding

When the user asks:

> "How many leaves can I carry forward?"

we also convert the **query** into an embedding.

```text
User Query
     ↓
Same Embedding Model
     ↓
Query Vector
```

This is important because now:

```text
Query Vector
      ↕
Document Vectors
```

exist in the same embedding space and can be compared.

---

# 13. Semantic Similarity

**Semantic = meaning.**

Semantic similarity asks:

> "How similar are these pieces of text in meaning?"

For example:

```text
"How many vacation days can I save?"
```

and:

```text
"How many paid leaves can I carry forward?"
```

use different words but have related meanings.

Embeddings help represent this relationship numerically.

---

# 14. Cosine Similarity

**Cosine similarity = a mathematical method for comparing two vectors.**

It essentially measures how similarly the vectors are pointing.

For example:

```text
A = [1, 2]
B = [2, 4]
```

They point in the same direction.

Therefore:

```text
cosine similarity = 1
```

### Important cases

```text
+1 → same direction
 0 → perpendicular directions
-1 → opposite direction
```

In our RAG system, cosine similarity helps determine which document chunks are more semantically similar to the user's query.

---

# 15. Keyword Similarity

We also calculate a simpler score based on overlapping words.

Example:

```text
Question:
"How many paid leaves?"

Document:
"Employees can carry forward paid leaves."
```

Common words include:

```text
paid
leaves
```

So the keyword score increases.

---

# 16. Hybrid Retrieval

Our system doesn't rely only on semantic similarity.

We combine:

```text
80% Semantic/Cosine Similarity
+
20% Keyword Similarity
```

Our code:

```python
combined_score = (
    0.8 * semantic_score
    + 0.2 * keyword_score
)
```

This approach is called:

> **Hybrid Retrieval**

It combines semantic understanding with keyword matching.

---

# 17. Similarity Threshold

Our current threshold is:

```text
0.65
```

But remember:

**0.65 is NOT a universal embedding threshold.**

In our application, it means:

```text
combined_score >= 0.65
```

is considered relevant enough to keep.

The threshold is an application parameter that can be tuned using evaluation.

---

# 18. Top-K Retrieval

We use:

```text
top_k = 3
```

**Top-K = number of highest-ranked results we want.**

Example:

```text
100 document chunks
       ↓
Similarity search
       ↓
Top 3 relevant chunks
```

We don't necessarily get one chunk from every document.

We get the **best relevant chunks across the vector store**.

---

# 19. Context

After retrieval, we take the relevant chunks and create:

```text
Context
```

Example:

```text
Company Context:
Employees can carry forward a maximum of
10 unused paid leaves to the next calendar year.
```

Then we combine:

```text
Context
+
User Question
+
Instructions
```

and send that to Gemini.

---

# 20. Grounding

**Grounding = keeping the LLM's answer based on reliable provided information.**

Our prompt tells Gemini:

```text
Answer using ONLY the company information
provided in the context.

Do not make up information.
```

So:

```text
RAG
 ↓
Find relevant information

Grounding
 ↓
Keep answer based on that information
```

RAG helps provide the evidence; grounding helps keep the response tied to that evidence.

---

# 21. Hallucination

**Hallucination = the AI generates information that isn't supported by the available information.**

Example:

Context says:

```text
Maximum carry-forward = 10 leaves
```

But Gemini answers:

```text
Maximum carry-forward = 15 leaves
```

That's an unsupported/hallucinated answer.

RAG + grounding can **reduce** hallucinations, but they don't guarantee that hallucinations will never happen.

---

# 22. Source Attribution

Our API returns the source:

```json
{
    "answer": "You can carry forward 10 leaves.",
    "sources": [
        {
            "filename": "leave_policy.txt",
            "chunk_id": 0
        }
    ]
}
```

This is called:

> **Source Attribution / Citation**

It tells us where the answer came from.

This is particularly useful in enterprise AI.

---

# 23. Evaluation

**Evaluation = testing whether our AI system is actually working correctly.**

We can test:

### Retrieval

Did we retrieve the correct document?

```text
Question → leave_policy.txt ✅
```

### Answer

Did Gemini produce the correct answer?

```text
Expected: 10
Generated: 10 ✅
```

### Groundedness

Is the answer supported by the retrieved context?

```text
Context: 10
Answer: 10
→ Grounded ✅
```

Evaluation becomes extremely important when building production AI systems.

---

# 24. Guardrails

**Guardrails = rules and controls that restrict unsafe, incorrect, or unauthorized AI behavior.**

Examples:

```text
Don't reveal confidential information.
Don't answer outside allowed knowledge.
Don't execute unauthorized actions.
Don't follow malicious instructions.
```

Guardrails can exist before and after the LLM and around tools.

---

# 25. API

**API = a way for software systems to communicate.**

Our user sends:

```http
POST /ask
```

with:

```json
{
    "question": "How many paid leaves can I carry forward?"
}
```

FastAPI processes it and returns:

```json
{
    "question": "...",
    "answer": "...",
    "sources": [...]
}
```

---

# 26. FastAPI

**FastAPI = Python framework for building APIs.**

Our architecture is:

```text
User / Frontend
       ↓
FastAPI
       ↓
RAG Pipeline
       ↓
Gemini
       ↓
FastAPI Response
```

We also use Swagger/OpenAPI through:

```text
/docs
```

to test our API.

---

# 27. Environment Variables

We store our Gemini API key in:

```text
.env
```

like:

```text
GEMINI_API_KEY=...
```

and read it using:

```python
os.getenv("GEMINI_API_KEY")
```

We don't put secrets directly into source code.

We also don't push `.env` to GitHub.

---

# 28. Deployment

We deployed the application using:

```text
GitHub
   ↓
Vercel
   ↓
FastAPI
   ↓
Gemini API
```

So our AI application is publicly accessible instead of running only on our local computer.

---

# ⭐ The Most Important Summary

If I had to reduce everything you've learned to one flow:

```text
                  DOCUMENTS
                      ↓
                   CHUNKING
                      ↓
                 EMBEDDINGS
                      ↓
               VECTOR STORE
                      │
                      │
                      ▼
                 USER QUERY
                      ↓
                 EMBEDDING
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
   COSINE SIMILARITY       KEYWORD SIMILARITY
          └───────────┬───────────┘
                      ↓
               HYBRID SCORE
                      ↓
              THRESHOLD + TOP-K
                      ↓
               RELEVANT CHUNKS
                      ↓
                   CONTEXT
                      ↓
             GROUNDING PROMPT
                      ↓
                  GEMINI LLM
                      ↓
              ANSWER + SOURCES
```

### Your current AI Engineering knowledge from this project

| Area                | Concepts learned                   |
| ------------------- | ---------------------------------- |
| **LLM**             | Gemini, generation                 |
| **RAG**             | Retrieval-Augmented Generation     |
| **Documents**       | Loading, knowledge base            |
| **Chunking**        | Document → chunks                  |
| **Embeddings**      | Text → vectors                     |
| **Vectors**         | Numerical semantic representation  |
| **Similarity**      | Cosine similarity                  |
| **Search**          | Semantic + keyword                 |
| **Retrieval**       | Hybrid retrieval, Top-K            |
| **Filtering**       | Similarity threshold               |
| **Context**         | Retrieved information → LLM        |
| **Grounding**       | Answer based on retrieved evidence |
| **Hallucination**   | Unsupported AI answers             |
| **Sources**         | Source attribution                 |
| **Evaluation**      | Measuring retrieval/answer quality |
| **Guardrails**      | Controlling AI behavior            |
| **Backend**         | Python, FastAPI, REST API          |
| **Security basics** | Environment variables/API keys     |
| **Deployment**      | GitHub + Vercel                    |

### 🧠 One sentence to remember

> **RAG takes a user's question, converts it into a vector, searches for semantically and/or lexically relevant document chunks, puts those chunks into the LLM's context, and asks the LLM to generate a grounded answer.*
