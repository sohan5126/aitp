# Check if Python is installed
$pythonVersion = python --version
if (!$?) {
    Write-Host "Python is not installed or not in PATH. Please install Python."
    exit
}

Write-Host "Setting up AI Photo Tagger Environment..."

# Create Virtual Environment if it doesn't exist
if (!(Test-Path -Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate Virtual Environment
Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

# Install Dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Run Server
Write-Host "Starting Server..."
Write-Host "Open your browser to: http://127.0.0.1:8000"
uvicorn backend.main:app --reload

