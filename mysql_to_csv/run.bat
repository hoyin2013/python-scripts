REM mysql_to_csv.bat
SET PATH=E:\oracle\instantclient_11_2;%PATH%
SET PATH=C:\Users\yinhb\AppData\Local\Programs\Python\Python37;%PATH%

SET WORK_DIR=%CD%
cd %WORK_DIR%
python mysql_to_csv.py 

@ECHO "Finished!"
pause
