class EmailManager(object):

    """docstring for EmailManager."""
    def __init__(self, configDict):
        self.configDict = configDict

    def getConnectionValidity(self):
        return True
