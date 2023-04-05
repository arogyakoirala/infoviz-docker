import requests
import json
import configparser
from StudentChecklistResponseParser import StudentChecklistResponseParser

DEFAULT_URL = "https://gateway.api.berkeley.edu/sis/v2/student-checklist/"

class StudentChecklistAPI :

    def __init__(self, baseUrl, configurationFilename):
        self.baseUrl = baseUrl
        self.configuration = self.loadConfiguration(configurationFilename)
        return

    def loadConfiguration(self, configurationFilename):
        configuration = {}
        config = configparser.ConfigParser()
        config.read(configurationFilename)
        configuration["app_id"] = config["studentChecklistAPI"]["app_id"]
        configuration["app_key"] = config["studentChecklistAPI"]["app_key"]
        return configuration

    def createHeaders(self):
        headers = {}
        headers["Accept"] = "application/json"
        headers["app_id"] = self.configuration["app_id"]
        headers["app_key"] = self.configuration["app_key"]
        return headers

    def createGetUrl(self, studentId):
        baseUrl = DEFAULT_URL
        if self.baseUrl is not None :
            baseUrl = self.baseUrl
        url = "{}/student/{}?id-type=campus-uid".format(baseUrl, studentId)
        #url = "{}/student/{}?id-type=uid".format(baseUrl, studentId)
        # print("########## ",url)
        return url

    def createPutUrl(self, studentId, checklistSeqId, itemSeqId):
        baseUrl = DEFAULT_URL
        if self.baseUrl is not None :
            baseUrl = self.baseUrl
        url = "{}/student/{}/list/{}/item/{}?id-type=campus-uid".format(baseUrl, studentId, checklistSeqId, itemSeqId)
        #url = "{}/student/{}/list/{}/item/{}?id-type=uid".format(baseUrl, studentId, checklistSeqId, itemSeqId)
        return url

    # Creates a Python dictionary object containing the payload necessary for
    # the PUT API -- identifies the item and the new status code for that item.
    def createPutPayload(self, itemName, statusCode):
        payload = {}
        payload["itemTypeCode"] = itemName
        payload["itemStatusCode"] = statusCode
        return payload

    def get(self, studentId):
        url = self.createGetUrl(studentId)
        headers = self.createHeaders()
        #print(url,headers)
        response = requests.get(url, headers=headers)
        #print("RESPONSE CODE={}".format(response.status_code))
        #print(response.text)
        return response

    def put(self, studentId, checklistSeqId, itemName, itemSeqId, statusCode):
        url = self.createPutUrl(studentId, checklistSeqId, itemSeqId)
        headers = self.createHeaders()
        payload = self.createPutPayload(itemName, statusCode)
        #print(url)
        #print(payload)
        response = requests.put(url, json=payload, headers=headers)
        return response
