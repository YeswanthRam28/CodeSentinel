# Project Manifest: CodeSentinel

## 1. The High Concept
**CodeSentinel** is not a chatbot. It is an **Autonomous AI DevOps Agent**.
It functions as a "Junior Developer" that lives in the cloud. You do not chat with it; you assign it tasks via GitHub Issues, and it performs the work asynchronously in a secure sandbox.

**The Golden Rule:** We are building an **Agentic Workflow** (Plan -> Act -> Observe -> Correct), not a conversational interface.

---

## 2. Core Architecture & Tech Stack

### A. The "Brain" (Orchestration)
* **Model:** Google Gemini 1.5 Flash (via API).
* **Orchestrator:** **LangGraph** (Stateful, cyclic graph architecture).
    * *Why:* We need loops (Reasoning -> Coding -> Testing -> Error -> Re-reasoning). Linear chains are insufficient.
* **Context Awareness:** **AST Parsing** (Abstract Syntax Tree) via `tree-sitter`.
    * *Why:* We map the repo structure symbolically (Classes, Functions) rather than just embedding raw text (RAG).

### B. The "Body" (Execution Environment)
* **Runtime:** **E2B Sandboxes** (Firecracker MicroVMs).
    * *Mechanism:* Every task spins up a fresh, isolated cloud sandbox.
    * *Security:* Network access is monitored. The sandbox is killed post-execution.
* **Backend:** **FastAPI** (Python). Handles webhooks, Sandbox management, and WebSocket streams.

### C. The "Face" (Frontend Experience)
* **Framework:** **Next.js 14** (App Router).
* **Styling:** **Tailwind CSS**.
* **Animation:** **Framer Motion** (Heavy usage for "smooth, tactile" feel).
* **Icons:** **Lucide React**.

---

## 3. The "God-Tier" Features (The Selling Points)

1.  **Symbolic Context Search (Not just RAG):**
    * Instead of blindly retrieving text chunks, CodeSentinel generates a "Skeleton" of the codebase to understand dependencies before writing a single line of code.

2.  **The Self-Healing Loop:**
    * *Step 1:* Agent writes code.
    * *Step 2:* Agent runs `pytest` or `npm test`.
    * *Step 3:* If tests fail, the Agent reads the stderr, analyzes the stack trace, and iterates on the code *automatically*.
    * *Limit:* Max 5 retries to prevent infinite loops.

3.  **Sandboxed Security:**
    * "What happens in E2B, stays in E2B." Malicious code generation cannot harm your local machine or the host server.

---

## 4. Design Language & Aesthetic (The "Awwwards" Vibe)

**Visual Identity:** "Cyber-Industrial," "Dark Mode SaaS," "Future-Utility."
**References:** Linear.app, Vercel, Raycast, Rauno.me.

### A. Color Palette
* **Background:** `bg-[#000212]` (Deep Void Black - slightly navy, not pure #000).
* **Primary Accent:** `text-[#5E6AD2]` (Indigo/Blurple) representing "Intelligence".
* **Success Accent:** `text-[#00FF94]` (Neon Spring Green) representing "Passing Tests".
* **Borders:** `border-white/10` (Subtle glassmorphism).

### B. Typography
* **Headings:** `Geist Sans` or `Inter` (Tight tracking `-0.02em`, font-weight 600).
* **Code/Logs:** `JetBrains Mono` or `Fira Code` (Consolas feel).

### C. Micro-Interactions (The "Juice")
* **The Terminal:** A floating 3D window that streams real logs (`> Cloning repo...`, `> AST Parsing...`). It must *feel* alive.
* **Bento Grids:** Feature cards arranged in an asymmetrical grid. Hovering reveals a "spotlight" gradient effect.
* **Glows:** Subtle radial gradients behind key elements to create depth. No flat colors.

---

## 5. User Journey (The "Happy Path")

1.  **Input:** User pastes a GitHub Issue URL into the Dashboard.
2.  **Planning:** The UI shows a "Thinking..." state. The Agent breaks the issue into sub-tasks.
3.  **Execution (The Show):**
    * The "Live Terminal" component streams the Agent's actions.
    * *User sees:* `> Docker container started [ID: a1b2]`
    * *User sees:* `> Reproducing bug... Failed (Good)`
    * *User sees:* `> Patching auth_controller.py...`
    * *User sees:* `> Running tests... Passed!`
4.  **Result:** The Agent generates a Pull Request link.
    * *UI:* A satisfying "Success" animation (Green confetti or glowing checkmark).

---

## 6. Prompting Instructions for AI (You)

* **When writing code:** Always prefer **Typescript** for Frontend and **Python 3.11+** for Backend.
* **When designing UI:** Do not use standard Tailwind colors. Use the specific hex codes defined above. Use `backdrop-blur-md` heavily.
* **Tone:** The copy should be confident, technical, and concise. No marketing fluff.
    * *Bad:* "Our tool helps you code better!"
    * *Good:* "Autonomous execution. Zero friction."