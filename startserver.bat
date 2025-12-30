REM REMOVED: startserver helper removed during revert












pausepython manage.py runserver
:: Run serverREM pip install -r grade_system\requirements.txt
:: Install requirements if not installed (optional)cd /d %~dp0
:: Ensure we're in project root (where manage.py lives))    call venv\Scripts\activate.batif exist venv\Scripts\activate.bat (:: Activate venv if exists