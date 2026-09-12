# Work flow

Suppose the user asks:

> **"How many paid leaves can I carry forward?"**

#### 1. Convert the query into a vector

```text
User Query
    ↓
Gemini Embedding Model
    ↓
Query Vector
```

This is **embedding**.

---

#### 2. Compare the query with our stored chunks

Our vector store already contains embeddings for the document chunks:

```text
leave_policy chunk → vector
wfh_policy chunk    → vector
it_support chunk    → vector
...
```

We compare the **query vector** against each chunk vector using:

```text
Cosine similarity
```

And we additionally calculate:

```text
Keyword similarity
```

Then we combine them:

```text
80% semantic similarity
+
20% keyword similarity
=
combined score
```

That's our **hybrid retrieval**.

---

#### 3. Apply the threshold

We currently have:

```text
threshold = 0.65
```

So chunks below that combined score are discarded.

The remaining chunks are considered relevant.

**Important:** We don't necessarily get "data from all three documents." We get the **top relevant chunks across the whole vector store**, up to `top_k=3`.

For example:

```text
leave_policy.txt   → 0.91 ✅
wfh_policy.txt     → 0.42 ❌
it_support.txt     → 0.31 ❌
```

Only the leave-policy chunk would be passed forward.

Or:

```text
leave_policy.txt   → 0.91 ✅
wfh_policy.txt     → 0.78 ✅
it_support.txt     → 0.70 ✅
```

Then all three could be included, because they're above the threshold and within `top_k=3`.

---

#### 4. Put those chunks into the prompt

We create something like:

```text
SYSTEM INSTRUCTION:
Answer using ONLY the provided company context.

CONTEXT:
Employees can carry forward a maximum of 10 unused
paid leaves to the next calendar year.

USER QUESTION:
How many paid leaves can I carry forward?
```

---

#### 5. Send that prompt to Gemini

```text
Prompt
  ↓
Gemini Generative Model
  ↓
Answer
```

Gemini responds:

> "You can carry forward a maximum of 10 unused paid leaves to the next calendar year."

---

### So remember this:

```text
              USER QUESTION
                    ↓
             EMBEDDING MODEL
                    ↓
              QUERY VECTOR
                    ↓
       ┌────────────┴────────────┐
       ↓                         ↓
Cosine Similarity         Keyword Similarity
       └────────────┬────────────┘
                    ↓
             Combined Score
                    ↓
           Threshold ≥ 0.65
                    ↓
              Top-K Chunks
                    ↓
              Build Context
                    ↓
             Gemini LLM API
                    ↓
             Generated Answer
```

And the terminology:

**Text → numbers = Embedding**

**Compare/search = Retrieval**

**Cosine + keyword = our Hybrid Retrieval**

**Relevant chunks = Context**

**Context + question → Gemini = Generation**

**Entire architecture = RAG**
