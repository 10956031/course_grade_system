REMOVED: start instructions removed during revert

3) 建議建立並啟用虛擬環境（如果還沒）：
   - Powershell:
       python -m venv venv
       .\venv\Scripts\Activate.ps1
   - CMD:
       python -m venv venv
       .\venv\Scripts\activate

4) 安裝需求：
   pip install -r grade_system\requirements.txt

5) 執行資料庫遷移（若需要）：
   python manage.py makemigrations
   python manage.py migrate

6) 建立 superuser（可選）：
   python manage.py createsuperuser

7) 啟動開發伺服器
   - 方式 A（手動）： python manage.py runserver
   - 方式 B（快速批次檔）： 執行 startserver.bat（在專案根目錄，會自動嘗試啟用 venv）

常見錯誤：
- 錯誤訊息 `python: can't open file 'C:\Users\user\manage.py'` 表示你沒有先切換到專案目錄。請先用 cd 進入含 `manage.py` 的資料夾後再執行 `python manage.py runserver`。

如果你希望我幫你直接在你的機器上跑一次指令並檢查錯誤輸出（你可以貼 terminal 的輸出），我可以一步步協助除錯。