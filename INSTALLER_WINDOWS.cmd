@echo off
setlocal
cd /d "%~dp0"

echo [1/5] Recherche de Python 3.12...
set "PYTHON312=%LocalAppData%\Programs\Python\Python312\python.exe"

if not exist "%PYTHON312%" (
    where py >nul 2>nul
    if errorlevel 1 goto python_missing
    for /f "delims=" %%P in ('py -3.12 -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON312=%%P"
)

if not exist "%PYTHON312%" goto python_missing
"%PYTHON312%" --version
if errorlevel 1 goto failed

echo.
echo [2/5] Suppression de l'ancien environnement...
if exist ".venv" rmdir /s /q ".venv"
if exist ".venv" goto failed

echo.
echo [3/5] Creation du nouvel environnement...
"%PYTHON312%" -m venv ".venv"
if errorlevel 1 goto failed

echo.
echo [4/5] Installation des dependances...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip install -r "requirements.txt"
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -m pip check
if errorlevel 1 goto failed

echo.
echo [5/5] Verification des notebooks...
set "TF_CPP_MIN_LOG_LEVEL=3"
set "CUDA_VISIBLE_DEVICES=-1"
set "MPLBACKEND=Agg"
".venv\Scripts\python.exe" "scripts\verify_notebooks.py"
if errorlevel 1 goto failed

echo.
echo ============================================================
echo INSTALLATION REUSSIE
echo Pour demarrer le cours :
echo .venv\Scripts\python.exe -m jupyter lab
echo ============================================================
if not defined COURSE_NO_PAUSE pause
exit /b 0

:python_missing
echo.
echo ERREUR : Python 3.12 est introuvable.
echo Installez Python 3.12 puis relancez ce fichier.
if not defined COURSE_NO_PAUSE pause
exit /b 1

:failed
echo.
echo ERREUR : l'installation a echoue.
if not defined COURSE_NO_PAUSE pause
exit /b 1
