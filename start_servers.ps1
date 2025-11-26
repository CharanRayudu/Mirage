$ErrorActionPreference = "Continue"

Write-Host "Starting Mirage Servers..." -ForegroundColor Cyan

# Start Backend (New Window)
Write-Host "Starting Backend (port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; uvicorn mirage.main:app --reload --port 8000"

# Start Frontend (New Window)
Write-Host "Starting Frontend (port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD/frontend'; npm run dev"

Write-Host "Servers started in separate windows." -ForegroundColor Green
