Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Job Search & Resume Matching - Server Start" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting FastAPI server on port 8006..." -ForegroundColor Yellow
Write-Host ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006

