@echo off
setlocal enabledelayedexpansion
REM ==============================================================
REM Author: Jason Hou
REM 
REM Date: 2013/07/13
REM 
REM Version: 0.4
REM 
REM Usage: 	this is a starter.
REM 		double click to run your MainCode through monkeyrunner
REM 
REM ************************ CHANGE HISTORY **********************
REM
REM VERSION : 0.4 Fourth Release 13-Jul-13 Jason Hou
REM REASON : Update implementation
REM REFERENCE : 
REM DESCRIPTION : 1. if not exist UserDefine.conf, create it, if not
REM					update logPath field
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


REM ************************User Define Section********************
set MainCode=Main.py
REM ************************User Define Section********************


if not exist %cd%\history mkdir history
set LOGPATH=logPath=%cd%\history
set OUTPATH=%cd%\config
set OUTNAME=UserDefine.conf
set OUTFILE=%OUTPATH%\%OUTNAME%
if not exist %OUTFILE% (
	echo [Path]>%OUTFILE%
	echo %LOGPATH%>>%OUTFILE%
) else (
	mv %OUTFILE% %OUTFILE%.bak
	for /f "delims=" %%N in (%OUTFILE%.bak) do (
		set line=%%N
		if "!line:~0,8!"=="logPath=" set line=%LOGPATH%
		echo !line!>>%OUTFILE%
	)
)
del %OUTFILE%.bak
echo Running, please wait!
monkeyrunner %cd%\%MainCode% 2>recorder.txt

REM --------------------------- end ------------------------------