$ErrorActionPreference = "Continue"

Write-Host "Starting Compliance Checks..." -ForegroundColor Cyan

# 1. Run Python Unit Tests
Write-Host "`n[1/5] Running Python Unit Tests..." -ForegroundColor Yellow
pytest mirage/tests
if ($LASTEXITCODE -ne 0) { Write-Host "Unit Tests Failed!" -ForegroundColor Red } else { Write-Host "Unit Tests Passed!" -ForegroundColor Green }

# 2. Run Pylint
Write-Host "`n[2/5] Running Pylint..." -ForegroundColor Yellow
# Ignoring some common errors for now to avoid noise, focusing on errors (E) and fatal (F)
pylint mirage/ --disable=C,R,W
if ($LASTEXITCODE -ne 0) { Write-Host "Pylint found issues." -ForegroundColor Red } else { Write-Host "Pylint Clean!" -ForegroundColor Green }

# 3. Run Black Check
Write-Host "`n[3/5] Checking Python Formatting (Black)..." -ForegroundColor Yellow
black --check mirage/
if ($LASTEXITCODE -ne 0) { Write-Host "Formatting issues found!" -ForegroundColor Red } else { Write-Host "Formatting Clean!" -ForegroundColor Green }

# 4. Run MyPy
Write-Host "`n[4/5] Running Type Checking (MyPy)..." -ForegroundColor Yellow
mypy mirage/ --ignore-missing-imports
if ($LASTEXITCODE -ne 0) { Write-Host "Type checking issues found!" -ForegroundColor Red } else { Write-Host "Type Checking Clean!" -ForegroundColor Green }

# 5. Frontend Linting
Write-Host "`n[5/5] Running Frontend Linting..." -ForegroundColor Yellow
cd frontend
npm run lint
cd ..

Write-Host "`nCompliance Checks Completed." -ForegroundColor Cyan
