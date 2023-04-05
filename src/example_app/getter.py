import configparser
import argparse
import requests
import json
from StudentChecklistResponseParser import StudentChecklistResponseParser
from StudentChecklistAPI import StudentChecklistAPI

DEFAULT_URL = "https://gateway.api.berkeley.edu/sis/v2/student-checklist"

def get(baseUrl, studentId):
    api = StudentChecklistAPI(baseUrl, "props.ini")
    return api.get(studentId)

def parseArguments() :
    parser = argparse.ArgumentParser(description="For the given student, return some checklist information")
    parser.add_argument("-s", metavar="studentId", type=int, help='the student ID number')
    parser.add_argument("-u", metavar="apiURL", default=DEFAULT_URL, help="alternate URL for the checklist API; defaults to the production URL")
    parser.add_argument("-c", metavar="checklistName", help="identifies the checklist by its sequence ID")
    parser.add_argument("-i", metavar="itemName", help="identifies the checklist item by its name")
    return parser.parse_args()

# Invoke the main method
if __name__ == '__main__':
    args = parseArguments()
    response = get(args.u, args.s)
    #print(response.text)
    parser = StudentChecklistResponseParser(response.text)
    code = parser.getStatus(args.c, args.i)
    if code == None:
        code = ""
    print(code)
