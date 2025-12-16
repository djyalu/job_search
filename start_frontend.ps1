Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Job Search & Resume Matching - Frontend Start" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
Write-Host ""
Write-Host "Starting React development server on port 3006..." -ForegroundColor Yellow
Write-Host ""
npm start

