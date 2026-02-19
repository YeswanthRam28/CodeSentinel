# 🌐 Deployment Guide: CodeSentinel

This guide provides step-by-step instructions for hosting the **CodeSentinel** autonomous agent in the cloud using **Render** (Backend) and **Vercel** (Frontend).

---

## 🔑 1. Prerequisites (API Keys)

Before deploying, ensure you have the following keys ready:

| Provider | Purpose | Link |
| :--- | :--- | :--- |
| **Google Gemini** | AI Brain (Fast reasoning) | [Get Gemini Key](https://aistudio.google.com/) |
| **GitHub** | Repository Cloning & PR creation | [Get PAT](https://github.com/settings/tokens) (Repo scope) |
| **E2B** | Cloud Sandboxing (Compute) | [Get E2B Key](https://e2b.dev/dashboard) |

---

## 🚀 2. Backend Deployment (Render)

Render will host the FastAPI server within a Docker container.

1.  **Sign up / Log in** to [Render](https://render.com/).
2.  Click **New +** > **Web Service**.
3.  Connect your GitHub repository.
4.  **Configure Service:**
    *   **Name:** `codesentinel-api` (or similar)
    *   **Root Directory:** `backend` (⚠️ CRITICAL)
    *   **Runtime:** `Docker`
5.  **Environment Variables:** Click "Advanced" and add:
    *   `GEMINI_API_KEY`: *Your Key*
    *   `GITHUB_TOKEN`: *Your GitHub PAT*
    *   `E2B_API_KEY`: *Your E2B Key*
    *   `PORT`: `8000`
6.  **Deploy:** Click **Create Web Service**.
7.  **Copy URL:** Once deployed, copy your URL (e.g., `https://codesentinel-api.onrender.com`).

---

## 🎨 3. Frontend Deployment (Vercel)

Vercel will build and host the React dashboard.

1.  **Sign up / Log in** to [Vercel](https://vercel.com/).
2.  Click **Add New** > **Project**.
3.  Import your GitHub repository.
4.  **Configure Project:**
    *   **Framework Preset:** `Vite` (Auto-detected)
    *   **Root Directory:** `./` (Root of the repo)
5.  **Environment Variables:** Add a new variable:
    *   `VITE_API_URL`: *Paste your Render URL from Step 2*
6.  **Deploy:** Click **Deploy**.

---

## ⚙️ 4. Local Verification & Cleanup

After deployment, your local repo may have build artifacts that should be cleaned up:

```bash
# Remove the manually pushed 'dist' folder
git rm -r --cached dist
git commit -m "chore: cleanup build artifacts for cloud hosting"
git push
```

---

## 💡 Troubleshooting & Tips

### 🕒 Render "Cold Start"
The Render Free Tier puts your backend to sleep after 15 minutes of inactivity. 
*   **Symptom:** The dashboard shows "Connection Error" on the first visit.
*   **Fix:** Wait ~60 seconds for the service to wake up and refresh the page.

### 🔌 WebSocket Issues
The Dashboard uses WebSockets (`/ws`) for the live terminal. 
*   If logs aren't streaming, ensure `VITE_API_URL` uses `https://` (Vercel) and the backend is correctly binding to `0.0.0.0`.

### 🛡 Security
*   **Never** commit your `.env` file to GitHub.
*   Ensure your **GitHub PAT** has the correct permissions to create Pull Requests on the target repositories you plan to analyze.
