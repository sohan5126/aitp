# How to Run Your AI Photo Tagger

Follow these steps to start the app yourself at any time.

## 1. Open Terminal
Open your standard Windows Terminal (PowerShell) or Command Prompt and navigate to the project folder:
```powershell
cd c:\Users\vinna\OneDrive\Documents\aitp
```

## 2. Start the Server
Run this command to start the app.
*Note: If you just updated the AI model, the first run might take 30-60 seconds to download it.*

```powershell
.\.venv\Scripts\uvicorn backend.main:app --reload
```

## 3. Open in Browser
Once you see "Application startup complete", open this link:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Troubleshooting
- **Port already in use?** If it fails saying the port is busy, make sure you closed any previous terminal windows running the server, or press `Ctrl + C` to stop the current one.
- **Connection Refused?** Make sure the terminal is open and the green "Uvicorn running..." text is visible.
