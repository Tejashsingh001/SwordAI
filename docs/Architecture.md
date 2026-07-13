# SwordAI Architecture

Version: 0.1

Status: Evolving

Last Updated: <13-07-2026>

Note:
This document represents the current architecture of SwordAI.
It is expected to evolve as the product grows and better ideas emerge.
Every major architectural change should be recorded in Decisions.md.

# 🏗 SwordAI Architecture

## Core Components

                  ┌────────────────────┐
                  │       USER         │
                  └─────────┬──────────┘
                            │
                            ▼
                ┌─────────────────────┐
                │   React Frontend    │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │  FastAPI Backend    │
                └─────────┬───────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │      Context & Memory Engine        │
        └───────┬───────────────────┬─────────┘
                │                   │
      retrieve/store          build context
                │                   │
                ▼                   ▼
┌────────────────────────┐   ┌────────────────────┐
│ Local Knowledge Base   │   │    AI Engine       │
│────────────────────────│   │────────────────────│
│ • User Knowledge       │   │ • Prompt Builder   │
│ • Projects             │   │ • Model Selector   │
│ • Knowledge Graph      │   │ • Token Optimizer  │
│ • Decisions            │   │ • Context Optimizer│
│ • Tasks                │   └─────────┬──────────┘
│ • Timeline             │             │
└──────────▲─────────────┘             ▼
           │               ┌───────────────────────┐
           └──────────────►│     AI Providers      │
                           │ Gemini • GPT • Claude │
                           │ Ollama                │
                           └──────────┬────────────┘
                                      │
                                      ▼
                     Response → Context & Memory Engine
                                      │
                                      ▼
                          Update Local Knowledge Base
                                      │
                                      ▼
                               Return Response

---

# Components

## 1. Frontend

The user interface where users interact with SwordAI.

Responsibilities:
- Chat
- Voice
- Project Management
- Settings
- File Uploads

---

## 2. Backend

Acts as the central controller.

Responsibilities:
- Receive user requests
- Coordinate all modules
- Connect frontend with the AI system
- Handle APIs

---

## 3. Context & Memory Engine

The brain of SwordAI.

Responsibilities:
- Detect what the user is asking.
- Identify related projects.
- Retrieve only relevant knowledge.
- Decide what new information should be saved.
- Update project knowledge after every conversation.

---

## 4. Local Knowledge Base

The permanent memory of SwordAI.

Stores:

- User Knowledge
- Projects
- Research
- Decisions
- Tasks
- Notes
- Timeline
- Knowledge Graph

This is the source of truth for the assistant.

---

## 5. AI Engine

Prepares requests for AI providers.

Responsibilities:

- Build optimized prompts
- Attach relevant context
- Select AI provider
- Reduce token usage

---

## 6. AI Provider

External AI model used for reasoning.

Examples:

- Gemini
- OpenAI
- Claude
- Ollama (Local)

The provider performs reasoning but does not permanently remember project information.

---

# Project Philosophy

Chats are **not** the source of truth.

Chats only create knowledge.

Knowledge is extracted and stored inside the Local Knowledge Base.

Projects exist independently of conversations.

A project can be continued from **any chat**, even outside the project's own folder.

---

# Request Flow

### Step 1

User asks:

```
Continue SwordAI
```

---

### Step 2

Backend receives the request.

---

### Step 3

Context & Memory Engine detects:

```
Project = SwordAI
Intent = Continue Development
```

---

### Step 4

Memory Engine retrieves:

- Current Stage
- Latest Decisions
- Architecture
- Tasks
- Timeline
- Relevant Notes

from the Local Knowledge Base.

---

### Step 5

AI Engine prepares an optimized prompt using only the required knowledge.

---

### Step 6

The request is sent to the selected AI Provider.

---

### Step 7

The AI Provider generates a response.

---

### Step 8

Before returning the response, the Memory Engine extracts any new important information.

Examples:

- New Decision
- Completed Task
- New Feature
- Architecture Update

---

### Step 9

The Local Knowledge Base is updated.

---

### Step 10

The final response is shown to the user.

The project is now ready to continue from **any conversation** in the future without relying on previous chat history.

---

# Core Principle

Knowledge is permanent.

Conversations are temporary.

The Local Knowledge Base is the single source of truth.

Every conversation contributes to the project's knowledge instead of becoming the project's memory.