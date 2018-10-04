import imaplib

import poplib
import string, random
#import StringIO
# import rfc822
import logging

class EmailManager(object):

    """docstring for EmailManager."""
    def __init__(self, configDict):
        # self.configDict = configDict
        self.FROM_EMAIL  = configDict["username"]
        self.FROM_PWD    = configDict["userpass"]
        self.POP_SERVER = configDict["popservername"]
        self.POP_PORT   = configDict["popserverport"]
        print(self.FROM_EMAIL)
        self.__connect()

    def __connect(self):
        try:
            self.server = poplib.POP3(self.POP_SERVER)
            self.server.user(self.FROM_EMAIL)
            self.server.pass_(self.FROM_PWD)
        except Exception as e:
            print(str(e))
            raise

    def getConnectionValidity(self):
        try:
            self.__checkMail()
            return True
        except Exception as e:
            return False

    def __checkMail(self):
        print("emailManager : __checkMail")
        try:
            pass
        except Exception as e:
            raise


class EmailImapManager(object):

    """docstring for EmailManager."""
    def __init__(self, configDict):
        # self.configDict = configDict
        self.FROM_EMAIL  = configDict["username"]
        self.FROM_PWD    = configDict["userpass"]
        self.SMTP_SERVER = "imap.gmail.com"
        self.SMTP_PORT   = 993
        print(self.FROM_EMAIL)

    def getConnectionValidity(self):
        try:
            self.__checkMail()
            return True
        except Exception as e:
            return False

    def __checkMail(self):
        print("emailManager : __checkMail")
        try:
            self.mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            self.mail.login(self.FROM_EMAIL,self.FROM_PWD)
            self.mail.list()
            self.mail.select('inbox')
            type, data = self.mail.search(None, 'ALL')
            self.id_list = data[0].split()
            if len(self.id_list) > 0:
                self.first_email_id = int(self.id_list[0])
                self.latest_email_id = int(self.id_list[-1])
            else:
                self.first_email_id = 0
                self.latest_email_id = 0
        except Exception as e:
            self.first_email_id = 0
            self.latest_email_id = 0
            print("Failed to login to mail with the following error:\n{}".format(str(e)))
