# Deployment Guide for Vision AI

This guide covers how to deploy the Vision AI application to common cloud platforms or run it with Docker.

## Option 1: Render.com (Recommended for Free Tier)

Render offers a free tier for web services that is perfect for this demo.

1.  **Push to GitHub**: Ensure your code is in a public or private GitHub repository.
2.  **Create Service**:
    *   Go to [dashboard.render.com](https://dashboard.render.com/).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.
3.  **Configure**:
    *   **Name**: `vision-ai-app` (or similar)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4.  **Deploy**: Click **Create Web Service**. It will take a few minutes to build.
5.  **Visit**: Once live, open the URL provided by Render.

## Option 2: Railway.app

Railway is another excellent option with a slightly different setup.

1.  **Push to GitHub**.
2.  **New Project**: Go to [railway.app](https://railway.app/) and start a new project from GitHub.
3.  **Deploy**: Railway usually detects the `Dockerfile` automatically and deploys it.
4.  **Verification**: If it doesn't auto-detect, go to settings and ensure the build command matches the Docker-based workflow or the Python workflow similar to Render.

## Option 3: Local Docker

If you have Docker Desktop installed, you can run the app in a container on your own machine.

1.  **Build Image**:
    ```bash
    docker build -t vision-ai .
    ```

2.  **Run Container**:
    ```bash
    docker run -p 8000:8000 vision-ai
    ```

3.  **Access**: Open `http://localhost:8000` in your browser.

## Troubleshooting

*   **Port Issues**: Docker maps port 8000 inside the container to 8000 on your machine. If that port is busy, change the run command to `-p 8080:8000` and visit port 8080.
*   **Slow First Request**: The AI model (`blip-image-captioning-base`) downloads on the first run. This behavior persists in containers unless configured with a persistent volume for the Hugging Face cache. On free tiers, this means the first request after a deployment/restart might take 30-60 seconds.
