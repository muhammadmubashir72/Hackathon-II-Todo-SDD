# Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud-Native AI

**Complete Detailed Guide (Full English Version in Markdown Format)**

This document contains the complete details of **Hackathon II** organized by Panaversity. It is an AI-native, spec-driven hackathon where participants progressively evolve a simple Todo application into a full cloud-native AI chatbot.

**Note:** The current date is January 02, 2026. The final submission deadline for the hackathon is January 18, 2026. If you're interested in participating, you still have time to complete and submit!

## Hackathon Introduction
The future of software development is AI-native and spec-driven. As AI agents (like Claude Code) grow more powerful, the engineer's role is shifting from "syntax writer" to "system architect."

In this hackathon, you will master **Spec-Driven Development**, **Claude Code**, **Reusable Intelligence**, and **Cloud-Native AI** technologies. You will start with a simple console app and end with a Kubernetes-deployed, AI-powered chatbot.

**Rewards & Opportunities:**  
Top performers may be invited to join the Panaversity core team (panaversity.org), become startup founders, and get teaching opportunities at PIAIC and GIAIC. You’ll work directly with founders Zia Khan, Rehan, Junaid, and Wania.

## What You Will Learn
- Spec-Driven Development using Claude Code and Spec-Kit Plus
- Reusable Intelligence: Agent Skills and Subagent Development
- Full-Stack Development: Next.js, FastAPI, SQLModel, Neon Serverless Database
- AI Agent Development: OpenAI Agents SDK and Official MCP SDK
- Cloud-Native Deployment: Docker, Kubernetes, Minikube, Helm Charts
- Event-Driven Architecture: Kafka and Dapr
- AIOps with kubectl-ai, kagent, and Claude Code
- Cloud-Native Blueprints for Spec-Driven Deployment

## Project: The Evolution of Todo
**Theme:** From CLI → Distributed Cloud-Native AI System  
**Goal:** Act as a Product Architect and build progressively complex software using AI, **without manually writing boilerplate code**.

**Core Rule:**  
- You **must** use **Spec-Driven Development** only.
- Write a **Markdown Constitution** and **Specs** for every feature.
- **No manual coding allowed** — refine specs until Claude Code generates correct implementation.

### Todo Features Levels
**Basic Level (Required):**
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark as Complete

**Intermediate Level:**
1. Priorities & Tags/Categories
2. Search & Filter
3. Sort Tasks

**Advanced Level:**
1. Recurring Tasks
2. Due Dates & Time Reminders (with browser notifications)

## Phases & Timeline

| Phase | Description                               | Technology Stack                                      | Points | Due Date      |
|-------|-------------------------------------------|-------------------------------------------------------|--------|---------------|
| I     | In-Memory Python Console App              | Python, Claude Code, Spec-Kit Plus                    | 100    | Dec 7, 2025   |
| II    | Full-Stack Web Application                | Next.js, FastAPI, SQLModel, Neon DB                   | 150    | Dec 14, 2025  |
| III   | AI-Powered Todo Chatbot                   | OpenAI ChatKit, Agents SDK, Official MCP SDK           | 200    | Dec 21, 2025  |
| IV    | Local Kubernetes Deployment               | Docker, Minikube, Helm, kubectl-ai, kagent             | 250    | Jan 4, 2026   |
| V     | Advanced Cloud Deployment                 | Kafka, Dapr, DigitalOcean DOKS (or AKS/GKE/OKE)        | 300    | Jan 18, 2026  |
| **Total** |                                       |                                                       | **1000** |             |

**Bonus Points (+600 possible):**
- Reusable Intelligence (Subagents & Skills) → +200
- Cloud-Native Blueprints via Agent Skills → +200
- Multi-language Support (Urdu in chatbot) → +100
- Voice Commands → +200

**Key Dates:**
- Hackathon Start: Dec 1, 2025
- Final Submission: Jan 18, 2026
- Live Presentations: Sundays at 8:00 PM (Dec 7, 14, 21, 2025; Jan 4 & 18, 2026)

## Submission Process
Submit each phase here: https://forms.gle/KMKEKaFUD6ZX4UtY8

Required for each submission:
1. Public GitHub Repository Link
2. Deployed App Link (Vercel / Chatbot URL)
3. Demo Video (under 90 seconds – judges watch only first 90s)
4. WhatsApp Number (for live presentation invites)

**Zoom Meeting for Presentations:**  
- Time: 8:00 PM on presentation Sundays  
- Link: https://us06web.zoom.us/j/84976847088?pwd=Z7t7NaeXwVmmR5fysCv7NiMbfbhIda.1  
- Meeting ID: 849 7684 7088  
- Passcode: 305850

## Detailed Phase Breakdown

### Phase I: In-Memory Python Console App
- Implement all 5 basic features
- In-memory storage only
- Deliverables: GitHub repo with `/specs` folder, `Constitution.md`, `CLAUDE.md`, README, working console demo

### Phase II: Full-Stack Web Application
- Multi-user web app with persistent storage
- Authentication using Better Auth (JWT-based)
- REST API with strict user isolation (tasks visible only to owner)
- Recommended: Monorepo structure (separate frontend/backend folders with shared Spec-Kit)

### Phase III: AI-Powered Todo Chatbot
- Natural language task management (e.g., "Reschedule my morning meeting to 2 PM")
- Use OpenAI Agents SDK + Official MCP SDK
- Expose task operations as MCP tools (add_task, list_tasks, complete_task, etc.)
- Stateless server; conversation history stored in DB
- Frontend: OpenAI ChatKit

### Phase IV: Local Kubernetes Deployment
- Containerize frontend and backend (use Gordon AI agent if available)
- Create Helm charts (generate via kubectl-ai/kagent)
- Deploy everything on Minikube locally

### Phase V: Advanced Cloud Deployment
- Implement Intermediate + Advanced features
- Event-driven architecture using Kafka (for reminders, recurring tasks, audit logs)
- Use Dapr for Pub/Sub, State Management, Jobs (scheduled reminders), Secrets
- Deploy to cloud Kubernetes (DigitalOcean recommended – $200 free credit)
- Set up CI/CD with GitHub Actions

## Key Tools & Resources
- Claude Code: https://claude.com/product/claude-code
- Spec-Kit Plus: https://github.com/panaversity/spec-kit-plus
- OpenAI ChatKit & MCP SDK
- Neon Serverless PostgreSQL (free tier)
- Vercel (frontend hosting)
- DigitalOcean Kubernetes ($200 credit for new accounts)
- Minikube, Helm, Dapr, Redpanda/Kafka

## Agentic Dev Stack Workflow
- Create comprehensive **AGENTS.md** (constitution for all AI agents)
- Use Spec-Kit Plus lifecycle: Specify → Plan → Tasks → Implement
- Set up MCP server to give Claude Code access to spec commands
- Use CLAUDE.md with `@AGENTS.md` reference for context

**Golden Rule:** No task = No code.

Good luck! May your specs be clear and your code be clean! 🚀

— The Panaversity, PIAIC, and GIAIC Teams