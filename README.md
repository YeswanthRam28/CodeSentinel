# CodeSentinel: Autonomous AI DevOps Agent

**CodeSentinel** is an autonomous AI developer that lives in your cloud. It's designed to function as a "Junior Developer" you can assign tasks to via GitHub Issues.

## 🚀 The Vision
CodeSentinel isn't a chatbot; it's an **Agentic Workflow**. It follows a cycle of **Plan -> Act -> Observe -> Correct** to solve engineering tasks asynchronously in a secure sandbox.

## 🧠 Key Features
- **Symbolic Context Search (✅ Implemented):** Uses AST parsing (`tree-sitter`) to understand repository structures and generates a structural "Skeleton" of classes and functions.
- **Repository Sandbox (✅ Implemented):** Clones any public GitHub repository into a secure, isolated Docker container for analysis.
- **Self-Healing Loop (✅ Implemented):** Uses LangGraph to orchestrate a recursive reasoning loop: Plan -> Research -> Code -> Test -> Correct. Automatically iterates until tests pass.
- **Sandboxed Security:** Executes all code within isolated Docker containers.
- **Next-Gen UI (✅ Implemented):** A premium, cyber-industrial dashboard built with React, Tailwind CSS, and Framer Motion, featuring a real-time WebSocket terminal.
- **Autonomous GitHub PRs (✅ Implemented):** Automatically creates Pull Requests on GitHub after verifying fixes in the sandbox.

## 🛠 Tech Stack
- **Brain:** LangGraph + Google Gemini 2.0 Flash
- **Execution:** Docker (Python SDK)
- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite, Tailwind CSS, Framer Motion, React Router, Lucide React

## 🏁 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.10+
- Docker (for agent execution)
- [Google Gemini API Key](https://aistudio.google.com/)
- [GitHub Personal Access Token](https://github.com/settings/tokens) (with `repo` scope)

### Setup & Installation

#### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/macOS
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env`:
   ```bash
   GEMINI_API_KEY=your_key
   GITHUB_TOKEN=your_token
   ```
5. Start the backend:
   ```bash
   python main.py
   ```

#### 2. Frontend Setup
1. In the root directory, install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Visit `http://localhost:3000` to access the Landing Page, then navigate to `/dashboard` to start tasks.

---
*Built with ❤️ for the future of autonomous engineering.*
