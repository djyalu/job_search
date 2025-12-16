@echo off
echo ======================================================================
echo Job Search & Resume Matching - Server Start
echo ======================================================================
echo.
echo Starting FastAPI server on port 8006...
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006
pause

