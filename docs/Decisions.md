Decision 001
Title

Knowledge-First Development Workflow

Decision

SwordAI will not rely on conversation history as the project's memory.

Every development session ends with an updated SESSION_STATE.md.

Reason

Knowledge should persist independently of conversations.

Future

SwordAI will generate and maintain this automatically.

Decision 002
Title

Architecture Freeze During Development

Decision

The architecture remains frozen during a development stage.

New ideas are stored in Ideas.md and reviewed only after the current stage is completed.

Reason

Prevents constant redesign and keeps development focused.

Future

Architecture is updated only when a major improvement is accepted.

Decision 003
Title

Unified Context & Memory Engine

Decision

SwordAI will use a single Context & Memory Engine instead of separate Context and Memory modules.

Reason

One component is responsible for understanding context, retrieving knowledge, extracting knowledge, and updating memory.

Future

The engine may internally evolve, but remains a single logical module.

Decision 004

Title

AI-Assisted Development Workflow

Decision

SwordAI architecture, product design, documentation, and technical decisions are created manually through planning sessions.

Codex is responsible for implementing approved code changes following the documented architecture and development rules.

Reason

This keeps architectural control with the developer while accelerating implementation without sacrificing understanding.

Future

As SwordAI matures, implementation may be distributed across multiple AI coding assistants while maintaining the same architecture-first workflow.

Decision 005
Title

Knowledge-Driven Development

Decision

SwordAI will always be designed around structured knowledge rather than conversation history.

Every new feature should integrate with the Local Knowledge Base whenever appropriate.

Reason

The project's core philosophy is that knowledge is permanent while conversations are temporary.

Future

The Memory Engine will continuously improve how knowledge is extracted and organized.

Decision 006
Title

Maintain CURRENT_STATE.md

Decision

SwordAI will maintain a CURRENT_STATE.md file containing the latest project structure, implemented features, APIs, models, database state, and current implementation progress.

Reason

It keeps development synchronized with the actual codebase and prevents duplicate implementations.

Future

SwordAI will generate and maintain this file automatically.

Decision 007
Title

Documentation Before Implementation

Decision

Major architectural decisions, workflows, and development rules should be documented before implementation begins.

Reason

Clear documentation improves consistency, collaboration, and long-term maintainability.

Future

SwordAI will eventually generate and update documentation automatically from the codebase.

Decision

Title:
Structured Conversation UI

Status:
Accepted

Reason:
Traditional AI chats become difficult to navigate during long-term projects.

Decision:
SwordAI will implement a tree-based conversation system where AI responses can contain nested discussion bubbles instead of extending the main conversation.

Implementation Stage:
Stage 6 (Frontend)

Status:
Frozen