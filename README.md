# CodeSentinel: Autonomous AI DevOps Agent

**CodeSentinel** is an autonomous AI developer that lives in your cloud. It's designed to function as a "Junior Developer" you can assign tasks to via GitHub Issues.

## 🚀 The Vision
CodeSentinel isn't a chatbot; it's an **Agentic Workflow**. It follows a cycle of **Plan -> Act -> Observe -> Correct** to solve engineering tasks asynchronously in a secure sandbox.

## 🧠 Key Features
- **Symbolic Context Search:** Uses AST parsing (`tree-sitter`) to understand repository structures, not just raw text.
- **Self-Healing Loop:** Automatically writes code, runs tests, analyzes failures, and iterates until the task is complete.
- **Sandboxed Security:** Executes all code within isolated Docker containers.
- **Next-Gen UI:** A premium, cyber-industrial dashboard built with Next.js 14, Tailwind CSS, and Framer Motion.

## 🛠 Tech Stack
- **Brain:** LangGraph + Google Gemini 1.5 Flash
- **Execution:** Docker (Python SDK)
- **Backend:** FastAPI (Python)
- **Frontend:** Next.js 14, Tailwind CSS, Lucide React

## 🏁 Getting Started

### Prerequisites
- Node.js
- Docker (for agent execution)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set your environment variables in `.env.local`:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```

---
*Built with ❤️ for the future of autonomous engineering.*
