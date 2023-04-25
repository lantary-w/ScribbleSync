@echo off
:loop
set /p filePath="Please input file path: "
python .\\core\main.py -f "%filePath%"
goto loop