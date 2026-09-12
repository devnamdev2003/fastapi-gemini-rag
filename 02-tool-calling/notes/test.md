Absolutely. Here are **practical test cases** you can save with your notes. Test them in Swagger at:

`http://127.0.0.1:8000/docs`

Start the application first:

```powershell
uvicorn app.main:app --reload
```

## 🧪 Test 1 — Leave Balance Tool

**Question:**

```text
How many leaves does employee 102 have?
```

**Expected tool:**

```text
get_leave_balance
```

**Expected result:**

```text
Employee 102 has 8 days of leave remaining.
```

---

## 🧪 Test 2 — WFH Tool

**Question:**

```text
How many WFH days has employee 102 used this week?
```

**Expected tool:**

```text
get_wfh_days
```

**Expected result:**

```text
Employee 102 has used 2 WFH days this week.
```

---

## 🧪 Test 3 — Multiple Tool Calling ⭐

This is one of the most important tests.

**Question:**

```text
Tell me the leave balance and WFH days used for employee 102.
```

**Expected tools:**

```text
get_leave_balance
get_wfh_days
```

**Expected result:**

```text
Employee 102:
- Leave balance: 8 days
- WFH days used this week: 2 days
```

This proves that the agent can use **multiple tools for one question**.

---

# 🧪 Test 4 — RAG

**Question:**

```text
How many paid leaves can an employee carry forward?
```

**Expected tool:**

```text
search_company_knowledge
```

The RAG system should find:

```text
Employees can carry forward a maximum of 10 unused paid leaves.
```

**Expected answer:**

```text
Employees can carry forward a maximum of 10 unused paid leaves
to the next calendar year.
```

---

# 🧪 Test 5 — WFH Policy Through RAG

**Question:**

```text
How many days per week can employees work from home?
```

**Expected tool:**

```text
search_company_knowledge
```

**Expected answer:**

```text
Employees can work from home up to 2 days per week.
```

---

# 🧪 Test 6 — IT Support RAG

**Question:**

```text
What should I do if my VPN is not working?
```

**Expected answer should be based on your IT support document:**

```text
First restart the VPN client and verify the internet connection.
If the problem continues, create an IT support ticket with a
description of the issue and relevant screenshots.
```

---

# 🧪 Test 7 — Tool + RAG Together ⭐⭐⭐

This is a very good **Agentic AI test**.

**Question:**

```text
Tell me employee 102's leave balance and whether the company
allows employees to carry forward unused leaves.
```

The agent should use:

```text
get_leave_balance
        +
search_company_knowledge
```

Expected information:

```text
Employee 102 has 8 days remaining.

The company allows employees to carry forward a maximum of
10 unused paid leaves to the next calendar year.
```

This proves your agent can combine:

**real-time employee data + company knowledge.**

---

# 🧪 Test 8 — Different Employee

**Question:**

```text
How many leaves does employee 101 have?
```

Expected:

```text
12 days
```

Then test:

```text
How many leaves does employee 103 have?
```

Expected:

```text
15 days
```

This confirms that the tool arguments are being generated correctly.

---

# 🧪 Test 9 — Unknown Employee

**Question:**

```text
How many leaves does employee 999 have?
```

Your current mock tool returns:

```text
0
```

because employee `999` doesn't exist in our sample dictionary.

This is also useful for understanding why **real production tools should validate whether the employee exists instead of treating missing data as zero**.

---

# 🧪 Test 10 — Question Outside Company Knowledge

**Question:**

```text
What is the company's maternity leave policy?
```

That information isn't present in our current documents.

Expected behavior:

```text
I don't have enough information in the company documents.
```

The important thing is:

> **The agent should not invent an answer.**

---

# 🧪 Test 11 — Question That Doesn't Need a Tool

**Question:**

```text
What is 10 + 20?
```

Expected behavior:

The agent should ideally answer directly rather than unnecessarily calling a company tool.

```text
30
```

This tests our instruction:

```text
Do not call tools unnecessarily.
```

---

# ⭐ Best 5 Tests to Remember

If you only want to keep five tests in your notes, keep these:

| Test | Question                                                        | Expected       |
| ---- | --------------------------------------------------------------- | -------------- |
| 1    | How many leaves does employee 102 have?                         | Leave tool     |
| 2    | How many WFH days has employee 102 used?                        | WFH tool       |
| 3    | Tell me leave balance + WFH days for 102                        | **Two tools**  |
| 4    | How many leaves can be carried forward?                         | **RAG tool**   |
| 5    | Tell me employee 102's balance and company carry-forward policy | **Tool + RAG** |

### The most important test

```text
Tell me employee 102's leave balance and whether the company
allows employees to carry forward unused leaves.
```

Expected architecture:

```text
                     User
                      ↓
                    Agent
                      ↓
              ┌───────┴────────┐
              ↓                ↓
     Leave Balance Tool       RAG
              ↓                ↓
       Employee Data     Company Documents
              └───────┬────────┘
                      ↓
                    Agent
                      ↓
                Final Answer
```

If this test works correctly, you've demonstrated the core idea of your **Agentic RAG application**.
