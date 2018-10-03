import os, unittest
import tests.utils.test_utils as test_utils
from src.configManager import ConfigManager

class ConfigManager_tests(unittest.TestCase):

    def setUp(self):
        self.configManager = ConfigManager(configFilePath = test_utils.configFilePath)

    def tearDown(self):
        #print("RoutesParser_tests: tearDown")
        pass

    def setUpClass():
        #print("RoutesParser_tests: setUpClass")
        pass

    def test_configFileIsParsed(self):
        self.assertTrue(len(self.configManager.getConfigDict()) > 0, "Failed to read config JSON!")

    def test_configHasEmailCredentials(self):
        requiredCredentials = [
        "username",
        "userpass",
        ]
        for credential in requiredCredentials:
            self.assertTrue(credential in self.configManager.getEmailCredentials(),
                            "Email config JSON has no {} credential!".format(str(credential)))
