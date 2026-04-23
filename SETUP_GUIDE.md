# Setup & Verification Guide: Multimedia AI Q&A

Follow this guide to get the platform running and verify its core functionalities.

## 📋 Prerequisites
Before you begin, ensure you have the following installed:
- **Docker & Docker Compose**: Essential for running the containerized services.
- **Node.js 20+**: (Optional) For running the frontend locally without Docker.
- **Maven**: (Optional) For running/testing the backend locally without Docker.
- **Google AI Gemini API Key**: Obtain one from [Google AI Studio](https://aistudio.google.com/).

---

## 🚀 Step-by-Step Setup

### 1. Project Initialization
Clone the repository and navigate to the project root:
```bash
git clone <repository-url>
cd ChiragProject
```

### 2. Environment Configuration
Create a `.env` file in the project root to store your secrets:
```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Build & Launch
Use Docker Compose to build and start the entire stack (PostgreSQL, Redis, Backend, Frontend):
```bash
docker-compose up --build
```
> [!NOTE]
> This process may take a few minutes as it downloads the base images and installs all dependencies.

---

## ✅ Verification Steps

### 1. Service Health Check
Verify that all services are up and running:
- **Frontend**: Navigate to `http://localhost:3000`. You should see the Multimedia AI dashboard.
- **Backend API**: Try `http://localhost:8080/api/media/123/timestamps`. You should get a 404 (file not found) or 401 (not authorized), indicating the server is responsive.

### 2. File Upload Test
1. Click the **"Upload New File"** button in the sidebar.
2. Select a sample PDF or MP4 video (max 50MB).
3. Wait for the processing to complete.
4. **Verification**: The file should appear in the "Your Files" list, and a summary should appear in the right sidebar.

### 3. RAG Chat Test
1. Select the uploaded file from the sidebar.
2. In the chat input, ask a specific question based on the content (e.g., "What are the main findings of this report?").
3. **Verification**: The AI should respond with a character-by-character streaming effect and cite sources using `[1]`, `[2]`, etc.

### 4. Multimedia Seek Test (For Video/Audio)
1. Upload a video file.
2. Look at the **"Topics & Timestamps"** section in the right sidebar.
3. Click on a timestamp (e.g., `01:15 - Core Concept`).
4. **Verification**: The integrated media player should seek directly to that second and begin playback.

---

## 🛠️ Troubleshooting

### Common Issues:
- **Docker Build Error**: Ensure you have enough disk space and a stable internet connection.
- **API Key Error**: If chat fails, check your Docker logs (`docker logs -f chiragproject-backend-1`). Look for "Invalid API Key".
- **Database Connection**: If the server fails to start, ensure no other process is using port `5432` or `6379`.
