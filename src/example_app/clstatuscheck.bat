@echo off

rem this returns the status of the specified checklist item given for the
rem person specified (UID), and the given checklist item (CLITEM) within
rem the specified checklist object (CLCODE)
rem usage: clstatuscheck UID CLCODE CLITEM
rem example: clstatuscheck 15182 GDISD GSURV1

set UID=%1
set CLCODE=%2
set CLITEM=%3

rem remcd B:\clu-uid-v2

:doit
getter.py -s %UID% -c %CLCODE% -i %CLITEM%

pause
