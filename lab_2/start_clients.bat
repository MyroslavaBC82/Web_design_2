@echo off

set CLIENT_COUNT=10

set /a CLIENT_COUNT=%CLIENT_COUNT%-1
for /l %%i in (1, 1, %CLIENT_COUNT%) do (
    start python main.py %%i
    timeout /t 1 /nobreak >NUL
)

set /a CLIENT_COUNT=%CLIENT_COUNT%+1
python main.py %CLIENT_COUNT%
