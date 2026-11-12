@echo off
setlocal
cd /d "%~dp0"
echo ==================================================
echo Nassau Candy Shipping Route Analysis
echo ==================================================
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul
  if %errorlevel%==0 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo Python was not found. Install Python 3.10 or newer from https://www.python.org/downloads/
      echo During installation, select "Add Python to PATH".
      pause
      exit /b 1
    )
    python -m venv .venv
  )
)
if not exist ".venv\Scripts\python.exe" (
  echo Could not create the virtual environment. Check your Python installation.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
if not exist ".venv\packages_installed.flag" (
  python -m pip install --upgrade pip
  if errorlevel 1 goto install_error
  python -m pip install -r requirements.txt
  if errorlevel 1 goto install_error
  echo installed> ".venv\packages_installed.flag"
)
echo.
echo Starting dashboard. Keep this window open while using it.
python -m streamlit run app.py
if errorlevel 1 goto run_error
goto end
:install_error
echo.
echo Package installation failed. Check your internet connection and try again.
pause
exit /b 1
:run_error
echo.
echo Dashboard did not start. Copy the error shown above and share it.
pause
exit /b 1
:end
pause
