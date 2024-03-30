@echo off
setlocal enabledelayedexpansion

REM Prompt the user for a custom commit summary
set /p custom_summary="Enter custom commit summary: "

REM Read the current number from the text file
set /p number=<commit_message.txt

REM Increment the number by one
set /a number+=1

REM Update the text file with the new number
echo %number%>commit_message.txt

git add .

REM Commit the changes with the custom summary and the new number as the message
git commit -m "Commit #%number% - %custom_summary%"

git push

REM Pause at the end
pause
