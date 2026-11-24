# SwordAI — PROJECT_STATE.md

**Last Updated:** 25 November 2026  
**Current Focus:** Backend testing

## 1. Project Vision

SwordAI is a Personal AI Operating System built around persistent knowledge and project context.

Core philosophy:
- Conversations are temporary. Knowledge is permanent.
- Knowledge is the source of truth, not conversations.
- Conversations create knowledge. Knowledge builds intelligence.

## 2. Architecture

Architecture remains frozen.

```text
React Frontend
      ↓
FastAPI Backend
      ↓
Routes
      ↓
Services
      ↓
AI Engine / Context & Memory Engine
      ↓
Context Retriever
      ↓
Prompt Builder
      ↓
AI Provider Client (Gemini currently)
      ↓
Response
      ↓
Memory Engine
      ↓
SQLite
```

Technology: React, FastAPI, Python, SQLAlchemy, SQLite, Pydantic, Gemini.

## 3. Current Development Progress

Previously implemented and audited:
- Stage 1: Foundation and core CRUD.
- Stage 2: Context & Memory Engine.
- Stage 3: AI integration and conversation system.

Current focus: Building a reliable automated testing suite before proceeding further.

## 4. Testing Infrastructure — Completed

Created:
- `backend/pytest.ini`
- `backend/requirements-test.txt`
- `backend/tests/conftest.py`
- `backend/tests/integration/test_infrastructure.py`

Features:
- In-memory SQLite database for tests.
- Isolated database sessions.
- FastAPI TestClient.
- Database dependency overrides.
- Protection against modifying production `swordai.db`.

## 5. Unit Tests — Completed

Files:

```text
backend/tests/unit/
├── __init__.py
├── test_project_task_schemas.py
├── test_knowledge_research_timeline_schemas.py
├── test_conversation_message_tag_schemas.py
├── test_memory_rules.py
├── test_conversation_message_tag_repositories.py
├── test_conversation_message_tag_services.py
└── test_core_crud_services.py
```

Coverage includes:

**Schemas**
- Project, Task, Research, Timeline, Knowledge.
- Conversation, Message, Tag and Dashboard responses.
- Validation, boundaries, defaults and invalid inputs.

**Memory rules**
- Extraction.
- Classification.
- Category precedence.
- Importance scoring and adjustments.

**Repositories and services**
- Conversation, Message and Tag repository operations.
- Conversation title generation and search.
- Pinning, archiving and restoring.
- Message persistence and summary refresh.
- Tag CRUD and conversation assignment.
- Project, Task, Knowledge, Research and Timeline service CRUD.

Important finding:
Project, Task, Knowledge, Research and Timeline repository classes do not currently exist. Their services directly perform SQLAlchemy operations. Tests correctly cover the existing service implementation instead.

<badge color="success">83 tests passed</badge>

Latest full-suite result:

```text
83 passed in 0.83s
```

No production database or external AI APIs were used. No application source code or business logic was modified.

## 6. Known Testing Gaps

Not yet tested:
- Dashboard repository/service.
- Memory Storage.
- Context Retriever.
- AI orchestration.
- API route integration.
- Long-title truncation.
- Every manual-summary transition.

Existing implementation concern:
- Core CRUD services accept `project_id` values without checking whether the Project exists.

Existing warnings:
- AnyIO/pytest compatibility.
- Pydantic v2 class-based configuration deprecations.
- SQLAlchemy model `datetime.utcnow()` deprecations.

## 7. Previous Audit Findings — Unresolved

- Decision CRUD API missing.
- User model/API incomplete.
- Some services bypass repositories.
- SQLite foreign-key enforcement not enabled.
- No database migration system.
- AI failures can leave partially saved interactions.
- Memory failures are logged and swallowed.
- Memory importance and timestamp handling inconsistencies.
- Duplicate unused `MemoryPromptBuilder` placeholder.
- Potentially misnamed `backend/app/routes/__.init__.py`.

These remain documented issues, not changes made during testing.

## 8. Next Session — Starting Point

Continue testing in this order:

1. Dashboard repository/service tests.
2. Memory Storage tests.
3. Context Retriever tests.
4. API CRUD integration tests.
5. Dashboard and conversation API regression tests.
6. AI Service and AI API tests with mocked Gemini responses.
7. Review coverage and remaining gaps.

Review existing implementation before writing each batch of tests.

## 9. Development Rules

- One Codex prompt at a time.
- Inspect → Implement → Review → Test.
- Do not modify application logic just to satisfy tests.
- Never use production database for tests.
- Mock external AI APIs.
- Keep architecture frozen unless explicitly changed.
- GitHub remains the source of truth.
- Update this file at the end of every development session.

**Architecture:** Unchanged.  
**Production database:** Protected.  
**Latest test result:** 83 passed.  
**Next task:** Dashboard, Memory Storage and Context Retriever testing.