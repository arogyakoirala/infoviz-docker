getter.bat - calls the checklist API via a python script to retrieve the status of a given checklist item (values returned are I or C for Initiated and Complete respectively).
required arguments:
UID
Checklist code
Checklist item code

clstatusupdate.bat - calls the checklist API via a python script to update the status of a given checklist item (usually will be used to update to a C - complete value).
required arguments:
UID
Checklist code
Checklist item code
Checklist item status code
