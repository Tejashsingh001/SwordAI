# ⚔️ SwordAI UI Architecture

Version: v1.0

Status: Frozen

Implementation Stage: Stage 6 (Frontend/UI)

---

# Vision

SwordAI is not a traditional chatbot.

The interface is designed around **projects**, **knowledge**, and **structured conversations**, rather than a long chronological chat.

The UI should feel like working inside an operating system for AI rather than chatting with a bot.

Core Principles

- Clean
- Minimal
- Project-focused
- Knowledge-first
- Context-aware
- Scalable

---

# UI Philosophy

Traditional AI

Conversation
↓

Long chat

↓

Information gets buried

↓

Context grows endlessly

↓

High token usage

SwordAI

Project
↓

Structured Conversation

↓

Knowledge

↓

Memory

↓

AI

The chat is only one way to interact with the system.

Knowledge is the center.

---

# Core UI Components

## Project Dashboard

Displays:

- Projects
- Recent Activity
- Recent Memories
- Timeline
- Tasks

Purpose

Entry point into SwordAI.

---

## Main Conversation

Contains only the primary discussion.

Should remain extremely clean.

Never polluted by clarification questions.

Every response is treated as a node.

---

## Structured Conversation System

Every AI response may contain child discussions.

Example

User

↓

AI Response

├── Discussion

├── Discussion

└── Discussion

Only the opened branch is visible.

---

# Discussion Bubble System

Every AI response displays

💬

or

💬 3

Clicking opens a floating discussion panel.

The panel contains:

User

↓

AI

↓

User

↓

AI

↓

...

Closing the panel returns to the main conversation.

The main conversation never grows because of clarification questions.

---

# Context Isolation

Each discussion receives only:

- Parent AI response
- Discussion history
- User question
- Relevant project memory

NOT

The entire conversation.

Benefits

- Lower token usage
- Better responses
- Faster retrieval
- Cleaner memory

---

# Conversation Tree

Internally

Root

│

├── Main Chat

│

├── AI Response

│      ├── Discussion A

│      │      └── Discussion A1

│      │

│      └── Discussion B

│

└── AI Response

Users only see the branch they open.

---

# Sidebar

Contains

- Projects
- Memories
- Knowledge
- Timeline
- Tasks
- Settings

The sidebar is the primary navigation component.

---

# Knowledge Viewer

Displays

- Saved Knowledge
- Categories
- Importance
- Related Projects

Supports

- Search
- Filters
- Sorting

---

# Memory Viewer

Displays

- Recent Memories
- Long-term Memories
- AI Generated Memories

Each memory should show

- Source Conversation
- Date
- Importance
- Related Project

---

# Timeline View

Displays project events chronologically.

Examples

Project Created

↓

Decision Saved

↓

Research Added

↓

Knowledge Generated

↓

Task Completed

---

# Search

Global search should retrieve

- Conversations
- Knowledge
- Research
- Timeline Events
- Tasks
- Decisions

Future

Semantic Search

---

# Response Actions

Every AI response can support actions.

Examples

💬 Discussion

📌 Pin

⭐ Save Knowledge

📝 Add Note

📋 Copy

↗ Expand

---

# Knowledge Extraction

Important discussions can become knowledge.

Flow

Discussion

↓

Extract Knowledge

↓

Knowledge Database

↓

Future Context

---

# Memory Integration

The UI should clearly indicate when AI uses memory.

Example

🧠 Used 4 related memories

Users may expand to view them.

---

# AI Transparency

When possible SwordAI should display

Current Context

Example

Project Memory

+

Timeline

+

Knowledge

+

Recent Discussion

This helps users understand why the AI answered a certain way.

---

# Theme

Modern

Minimal

Dark-first

Rounded Components

Smooth Animations

Low Visual Noise

Focus should remain on content.

---

# Navigation Principles

Maximum two clicks to reach any major feature.

Never lose project context.

Always know

- Current Project
- Current Discussion
- Current Memory Source

---

# Future Enhancements

- Multi-panel workspace
- Split conversations
- AI-generated summaries
- Discussion merging
- Knowledge graph visualization
- Semantic search
- Collaborative editing
- Voice interaction
- Plugin system
- Custom dashboards

---

# Design Principles

1. Keep the main conversation clean.

2. Discussions are isolated.

3. Knowledge is permanent.

4. Memory is transparent.

5. Projects are the center of the experience.

6. UI should reduce cognitive load.

7. Navigation should be intuitive.

8. AI should explain where information comes from.

---

# Product Identity

SwordAI is not designed to replace ChatGPT.

SwordAI is designed to become a personal AI Operating System capable of remembering projects, organizing knowledge, and supporting long-term development through structured conversations and intelligent memory management.

---

# Status

Version: v1.0

Architecture Status: Frozen

Implementation Stage: Stage 6 (Frontend)

Owner: SwordAI Project