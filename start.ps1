# ======================================
# 🎓 LegendBot School Inquiry Assistant
# ======================================

Write-Host "Starting the application..."
Write-Host ""

# --- Check for Python ---
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python 3 is not installed. Please install Python 3 first." -ForegroundColor Red
    exit 1
}

# --- Check if app.py exists ---
if (-not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found. Please run this script from the project directory." -ForegroundColor Red
    exit 1
}

# --- Install dependencies ---
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip3 install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting LegendBot server..." -ForegroundColor Cyan
Write-Host "📱 Application will be available at: http://localhost:5000"
Write-Host "🛑 Press Ctrl+C to stop the server"
Write-Host ""

# --- Run the Flask app ---
python3 app.py
