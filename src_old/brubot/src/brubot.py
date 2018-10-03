#global imports
import _thread
import time

# local imports
import configManager as configManager
import emailManager as emailManager
import logManager as logManager
import torrentManager as torrentManager


class Brubot(object):
    """docstring for Brubot"""

    def __init__(self):
        print("Brubot initialized!")
        self.DBNAME = "brubot.db"
        self.DBNAME = 'example.db'
        self.configManager  = configManager.configManager(self.DBNAME)
        self.emailManager   = emailManager.emailManager(emailAddress = self.configManager.getEmailUser(),
                                                        emailPass = self.configManager.getEmailPass())
        self.logManager     = logManager.logManager()
        self.torrentManager = torrentManager.torrentManager()

    def start(self):
        print("Brubot started!")
        self.configManager.start()
        self.emailManager.start()
        self.logManager.start()
        self.torrentManager.start()

    def close(self):
        print("Brubot closed!")
        self.configManager.close()
        self.emailManager.close()
        self.logManager.close()
        self.torrentManager.close()

    def checkStatus(self):
        print("Brubot: check status")
        self.emailManager.getAllMails()
        if self.emailManager.getMailsCount() != 0:
            # while (getOldestEmail)
            message = self.emailManager.getOldestEmail()

        # process it (store job in db)

            # remove it
            self.emailManager.deleteOldestEmail()

        # loop through db and check status for current waiting jobs

if __name__ == '__main__':
    print("brubot: start from main")
    brubot = Brubot()
    while True:
        time.sleep(5)
        brubot.checkStatus()
