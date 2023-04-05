@echo off

rem for a given person (UID), this changes the status code (STCODE) of the
rem specified checklist item (CLITEM) within the specified checklist object
rem (CLCODE)
rem usage: clstatusupdate UID CLCODE CLITEM STCODE
rem example: clstatusupdate 15182 GDISD GSURV1 C

set UID=%1
set CLCODE=%2
set CLITEM=%3
set STCODE=%4

cd B:\clu-uid-v2

:doit
chup.py -s %UID% -c %CLCODE% -i %CLITEM% -x %STCODE%

pause
