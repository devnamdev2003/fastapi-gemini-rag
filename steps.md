## 🚀 Deploy a new FastAPI app to Vercel

### Step 1 — Prepare your project

A simple structure should look like:

```text
my-ai-project/
├── api/
│   └── index.py
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── ...
├── requirements.txt
├── .gitignore
└── .env
```

Your `api/index.py`:

```python
from app.main import app
```

And make sure `app/__init__.py` exists.

---

### Step 2 — Create `requirements.txt`

For example:

```text
fastapi
uvicorn
python-dotenv
google-genai
```

Add any other packages your project actually uses.

---

### Step 3 — Create `.gitignore`

At minimum:

```text
venv/
.venv/
__pycache__/
.env
*.pyc
```

**Important:** Never push your `.env` or API keys to GitHub.

---

### Step 4 — Test locally first

Activate your virtual environment:

```powershell
venv\Scripts\activate
```

Then run:

```powershell
uvicorn app.main:app --reload
```

Check:

```text
http://127.0.0.1:8000/docs
```

Make sure the API works **before deploying**.

---

### Step 5 — Push the project to GitHub

Create a new GitHub repository.

Then:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

---

### Step 6 — Import the GitHub repo into Vercel

Go to [Vercel](https://vercel.com/?utm_source=chatgpt.com)

Then:

**Add New → Project → Import Git Repository**

Select your GitHub repository.

Usually:

```text
Framework Preset: Python
Root Directory: ./
Install Command: pip install -r requirements.txt
Build Command: None
Output Directory: N/A
```

Then deploy.

---

### Step 7 — Add environment variables

If your application uses an API key:

**Vercel → Project → Settings → Environment Variables**

For example:

```text
GEMINI_API_KEY = your_actual_key
```

Select:

```text
Production
Preview
```

Then redeploy if necessary.

**Never put the actual key inside your Python code or GitHub repository.**

---

### Step 8 — Test the deployed API

For our current architecture, test the Vercel endpoint, for example:

```text
https://your-project.vercel.app/api/
```

and:

```text
https://your-project.vercel.app/api/docs
```

The exact URL depends on how your Vercel entrypoint is structured.

---

## ⭐ The important thing you should remember

For your current project, the key Vercel pattern is:

```text
GitHub
   ↓
Vercel
   ↓
api/index.py
   ↓
app/main.py
   ↓
FastAPI
   ↓
Your AI application
```

So whenever you create another FastAPI AI project, **don't create a root `app.py` if you're using the `app/` package + `api/index.py` structure**. That's what caused the deployment problem we just fixed.

### Your reusable checklist

```text
☑ FastAPI project works locally
☑ requirements.txt
☑ .gitignore
☑ .env NOT pushed to GitHub
☑ app/__init__.py
☑ api/index.py
☑ Push to GitHub
☑ Import repo into Vercel
☑ Add API keys in Vercel Environment Variables
☑ Deploy
☑ Test /api/ and /api/docs
```