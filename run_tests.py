from tests.unit.configManager_tests import ConfigManager_tests
from tests.unit.emailManager_tests import EmailManager_tests
import unittest

if __name__ == '__main__':
    suites = [
             unittest.TestLoader().loadTestsFromTestCase(ConfigManager_tests),
             unittest.TestLoader().loadTestsFromTestCase(EmailManager_tests),
             ]

    for suite in suites:
        unittest.TextTestRunner(verbosity=2).run(suite)
