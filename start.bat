@echo off
REM ==============================================================
REM Author: Jason Hou
REM 
REM Date: 2013/07/09
REM 
REM Version: 0.3
REM 
REM Usage: 	this is a starter.
REM 		double click to run your MainCode through monkeyrunner
REM 
REM ************************ CHANGE HISTORY **********************
REM
REM VERSION : 0.3 Third Release 09-Jul-13 Jason Hou
REM REASON : Update implementation
REM REFERENCE : 
REM DESCRIPTION : 1. output the runtime info in terminal real time 
REM					and output exception to recorder.txt
REM
REM VERSION : 0.2 Second Release 07-Jul-13 Jason Hou
REM REASON : Update implementation
REM REFERENCE : 
REM DESCRIPTION : 1. Create history folder if not exist under current path 
REM 			  2. Write path info into UserDefine.conf
REM
REM VERSION : 0.1 First Release 03-Jul-13 Jason Hou
REM REASON : First implementation
REM REFERENCE : 
REM DESCRIPTION : 1. Create the starter to start MainCode instead 
REM 				of typing command in terminal 
REM
REM ==============================================================
REM -------------------------- start -----------------------------

set MainCode=Main.py
cd %cd%
if not exist %cd%\history mkdir history
echo [Path]>%cd%\config\UserDefine.conf
echo logPath=%cd%\history>>%cd%\config\UserDefine.conf
echo Running, please wait!
monkeyrunner %cd%\%MainCode% 2>recorder.txt
::echo Completed! Press any key to exit!
pause

REM --------------------------- end ------------------------------