import json
import sys

class ChecklistItemUtils:

    def getName(self, item):
        return item["type"]["code"]

    def getSequenceNumber(self, item):
        return item["sequenceNumber"]

    # Returns the tuple indicating this item's status: {code, description}
    def getStatus(self, item):
        return item["status"]

    def getItems(self, checklist):
        try:
            return checklist["items"]
        except KeyError:
            return None

    # Returns a dictionary of the most recent of each type of checklist in the
    # GET response
    def getSummary(self, checklist):
        items = self.getItems(checklist)
        if items == None:
            return None
        mapp = {}
        for item in items:
            if item["type"] == {}:
                 return("Checklist found but not the item")
            name = self.getName(item)
            sequenceNumber = self.getSequenceNumber(item)
            if name not in mapp or (name in mapp and mapp[name] < sequenceNumber):
                mapp[name] = sequenceNumber
        return mapp

    # Return an item summary for an item with the given name.  If more than one
    # item has the given name, return the sequence number of the item that has
    # the highest sequence number.
    def getItem(self, checklist, name):
        items = self.getItems(checklist)
        if items == None:
            return None
        summary = self.getSummary(checklist)
        if summary == None:
            return None
        if name in summary:
            sequenceNumber = summary[name]
            for item in items:
                if self.getName(item) == name and self.getSequenceNumber(item) == sequenceNumber:
                    return item
        return None



class ChecklistUtils:

    def getName(self, checklist):
        return checklist["type"]["code"]

    def getSequenceNumber(self, checklist):
        return checklist["sequenceNumber"]

    def getAdministrativeFunction(self, checklist):
        return checklist["administrativeFunction"]

    def getType(self, checklist):
        return checklist["type"]

    def getStatus(self, checklist):
        return checklist["status"]

    def getStatusDate(self, checklist):
        return checklist["statusDate"]

    def getStatusUpdatedBy(self, checklist):
        return checklist["statusUpdatedBy"]

    def getDueDate(self, checklist):
        return checklist["dueDate"]

    def getResponsibleParty(self, checklist):
        return checklist["responsibleParty"]

    def getVariableData(self, checklist):
        return checklist["variableData"]

    def getItems(self, checklist):
        checklistItemUtils = ChecklistItemUtils()
        return checklistItemUtils.getItems(checklist)

    # Returns a dictionary of the most recent of each type of checklist in the
    # GET response
    def getSummary(self, checklists):
        if checklists == None:
            return None
        mapp = {}
        for checklist in checklists:
            name = self.getName(checklist)
            sequenceNumber = self.getSequenceNumber(checklist)
            if name not in mapp or (name in mapp and mapp[name] < sequenceNumber):
                mapp[name] = sequenceNumber
        return mapp


class StudentChecklistResponseParser:
    def __init__(self, jsonBody):
        self.jsonBody = jsonBody
        #blah = jsonBody.encode(sys.stdout.encoding, errors='replace')
        #sourceFile = open('demo1.html', 'w')
        #print(blah, file = sourceFile)
        #sourceFile.close()
        self.jsonParsed = json.loads(jsonBody)

    def getHttpStatus(self):
        try:
            return self.jsonParsed["apiResponse"]["httpStatus"]
        except KeyError:
            return None

    def getChecklists(self):
        try:
            return self.jsonParsed["apiResponse"]["response"]["studentChecklists"][0]["checklists"];
        except KeyError:
            return None

    # Returns the checklist with the given name and highest sequence number
    def getChecklist(self, name):
        checklistUtils = ChecklistUtils()
        checklists = self.getChecklists()
        #print(checklists)
        summary = checklistUtils.getSummary(checklists)
        if summary == None:
            return None
        if name not in summary:
            return None
        sequenceNumber = summary[name]
        for checklist in checklists:
            if checklistUtils.getName(checklist) == name:
                if checklistUtils.getSequenceNumber(checklist) == sequenceNumber:
                    return checklist
        return None

    # Given a checklist's name and an item's name in that checklist, return a
    # dictionary containing the sequence numbers for that checklist and item.
    def getSequenceNumbers(self, checklistName, itemName):
        checklistUtils = ChecklistUtils()
        checklistItemUtils = ChecklistItemUtils()
        checklist = self.getChecklist(checklistName)
        if checklist == None:
            return("CLERR")
        item = checklistItemUtils.getItem(checklist, itemName)
        if item == None:
            return("CLIERR")
        numbers = {}
        numbers["checklist"] = checklistUtils.getSequenceNumber(checklist)
        numbers["item"] = checklistItemUtils.getSequenceNumber(item)
        numbers[checklistName] = checklistUtils.getSequenceNumber(checklist)
        numbers[itemName] = checklistItemUtils.getSequenceNumber(item)
        return numbers

    # Given a checkist's name and an item's name within that checklist,
    # return the status code for that item within the checklist.
    def getStatus(self, checklistName, itemName):
        checklistUtils = ChecklistUtils()
        checklistItemUtils = ChecklistItemUtils()
        checklist = self.getChecklist(checklistName)
        if checklist == None:
            return("Checklist " + checklistName + " not found")
            #return None
        item = checklistItemUtils.getItem(checklist, itemName)
        if item == None:
            return("Checklist item " + itemName + " not found")
        status = checklistItemUtils.getStatus(item);
        return status["code"]
 
