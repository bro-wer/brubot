import json

class ConfigManager(object):
    """docstring for ConfigManager."""
    def __init__(self, configFilePath):
        self.configDictFilePath = configFilePath
        self.configDict = {}
        self.__extractJson()

    def __extractJson(self):
        with open(self.configDictFilePath) as f:
            self.configDict = json.load(f)

    def getConfigDict(self):
        return self.configDict

    def getEmailCredentials(self):
        return self.configDict["email"]


#{
#  "email" : {
#    "username":"",
#    "userpass":""
#  }
#}
#
