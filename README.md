# CodeSentinel: Autonomous AI DevOps Agent

**CodeSentinel** is an autonomous AI developer that lives in your cloud. It's designed to function as a "Junior Developer" you can assign tasks to via GitHub Issues.

## 🚀 The Vision
CodeSentinel isn't a chatbot; it's an **Agentic Workflow**. It follows a cycle of **Plan -> Act -> Observe -> Correct** to solve engineering tasks asynchronously in a secure sandbox.

## 🧠 Key Features
- **Symbolic Context Search (✅ Implemented):** Uses AST parsing (`tree-sitter`) to understand repository structures and generates a structural "Skeleton" of classes and functions.
- **Universal Sandbox (✅ Implemented):** Isolated E2B Cloud Sandboxes (Firecracker microVMs) with **Smart Dependency Detection** (Python, Node.js, and static checks).
- **Self-Healing Loop (✅ Implemented):** Uses LangGraph to orchestrate a recursive reasoning loop: Plan -> Research -> Code -> Test -> Correct.
- **Cyber-Industrial Dashboard (✅ Implemented):** A premium Dark Mode UI built with React + Framer Motion, featuring a real-time, autoscrolling WebSocket terminal.
- **Autonomous GitHub PRs (✅ Implemented):** Automatically creates Pull Requests on GitHub after verifying fixes in the sandbox.

## 🛠 Tech Stack
- **Brain:** LangGraph + NVIDIA API (Moonshot Kimi-K2)
- **Execution:** E2B Cloud Sandboxes
- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite, Tailwind CSS, Framer Motion

## 🏁 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.10+
- [E2B API Key](https://e2b.dev/dashboard)
- [NVIDIA API Key](https://build.nvidia.com/moonshotai/kimi-k2-instruct)
- [GitHub Personal Access Token](https://github.com/settings/tokens) (repo scope)

### Setup & Installation

#### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1 # Windows
   source venv/bin/activate    # Linux/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env`:
   ```bash
   NVIDIA_API_KEY=your_key
   GITHUB_TOKEN=your_token
   E2B_API_KEY=your_e2b_key
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
