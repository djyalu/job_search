@echo off
echo ======================================================================
echo Job Search & Resume Matching - Frontend Start
echo ======================================================================
echo.
echo Installing dependencies...
cd frontend
call npm install
echo.
echo Starting React development server on port 3006...
echo.
call npm start
pause

