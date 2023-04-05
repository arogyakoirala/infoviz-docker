import argparse
import requests
import json
import sys
from StudentChecklistAPI import StudentChecklistAPI
from StudentChecklistResponseParser import StudentChecklistResponseParser

DEFAULT_URL = "https://gateway.api.berkeley.edu/sis/v2/student-checklist"

def parseArguments() :
    parser = argparse.ArgumentParser(description="For the given student, check an item off the SIS checklist")
    parser.add_argument("-s", metavar="studentId", type=int, help='the student ID number')
    parser.add_argument("-c", metavar="checklistName", help="identifies the checklist by its sequence ID")
    parser.add_argument("-i", metavar="itemName", help="identifies the checklist item by its name")
    parser.add_argument("-x", metavar="statusCode", help="specifies the new status for the checklist item")
    parser.add_argument("-u", metavar="apiURL", default=DEFAULT_URL, help="alternate URL for the checklist API; defaults to the production URL")
    return parser.parse_args()


def go(baseUrl, studentId, checklistName, itemName, statusCode):
    api = StudentChecklistAPI(baseUrl, "props.ini")

    # First, get the student's checklist info
    response = api.get(studentId)

    # debug, print to file
    #blah = response.text.encode(sys.stdout.encoding, errors='replace')
    #sourceFile = open('demo.html', 'w')
    #print(blah, file = sourceFile)
    #sourceFile.close()

    # Use the response parser to peel off the sequence numbers
    parser = StudentChecklistResponseParser(response.text)
    sequenceNumbers = parser.getSequenceNumbers(checklistName, itemName)
    if sequenceNumbers == "CLERR":
        return("CLERR")
    if sequenceNumbers == "CLIERR":
        return("CLIERR")
    else:
        # JR: not working anymore in V2 API.
        # Pull out the sequence numbers for our checklist and our item
        #checklistSeqId = sequenceNumbers[checklistName]
        #itemSeqId = sequenceNumbers[itemName]

        # Pull out the sequence numbers for our checklist and our item
        checklistSeqId = sequenceNumbers['checklist']
        itemSeqId = sequenceNumbers['item']

        # Use the sequence numbers to update the checklist
        return api.put(studentId, checklistSeqId, itemName, itemSeqId, statusCode)

# Invoke the main method
if __name__ == '__main__':
    args = parseArguments()
    response = go(args.u, args.s, args.c, args.i, args.x)

    if response == "CLERR":
        print("Checklist " + args.c + " not found for ID " + str(args.s))
    else:
        if response == "CLIERR":
            print("Checklist item " + args.i + " not found for ID " + str(args.s))
        else:
            print(response)
            print(response.text)
