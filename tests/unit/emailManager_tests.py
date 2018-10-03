import os, unittest
import tests.utils.test_utils as test_utils
from src.configManager import ConfigManager
from src.emailManager import EmailManager

#class EmailManager_tests(unittest.TestCase):
class EmailManager_tests(unittest.TestCase):

    def setUp(self):
        self.configManager = ConfigManager(configFilePath = test_utils.configFilePath)
        self.emailManager = EmailManager(configDict = self.configManager.getEmailCredentials())

    def tearDown(self):
        #print("RoutesParser_tests: tearDown")
        pass

    def setUpClass():
        #print("RoutesParser_tests: setUpClass")
        pass

    def test_canConnectWithEmail(self):
        self.assertTrue(self.emailManager.getConnectionValidity() == True, "Failed to read config JSON!")
