@echo off
cd /d %~dp0

call venv\Scripts\activate

REM Launch app in same window
python app.py
