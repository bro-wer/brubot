import smtplib
import time
import imaplib
import email
import datetime

class emailManager(object):

    """docstring for [object Object]."""
    def __init__(self, emailAddress, emailPass):
        self.ORG_EMAIL   = "@" + str(emailAddress).split("@")[1]
        self.FROM_EMAIL  = emailAddress
        self.FROM_PWD    = emailPass
        self.SMTP_SERVER = "imap.gmail.com"
        self.SMTP_PORT   = 993
        print("Starting emailManager...")

    def start(self):
        pass

    def close(self):
        print("Closing emailManager...")

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

    def getAllMails(self):
        print("emailManager : getAllMails")
        self.__checkMail()

        for num in self.id_list:
            rv, data = self.mail.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("No messages found!")
                return

            data = data[0][1].decode('utf-8')
            msg = email.message_from_string(data)
            decode = email.header.decode_header(msg['Subject'])[0]
            subject = decode[0]
            # print("\n\n########################################")
            #print("Message {}:{}".format(str(num), subject))
            #print("Raw date :{}".format(str(msg['Date'])))
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                print ("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            #for key in msg.keys():
            #    print(key)
            while msg.is_multipart():
                msg = msg.get_payload(0)
            msgTxt = msg.get_payload(None, True).decode('utf-8')
            # print(str(msgTxt))

    def getOldestEmail(self):
        if len(self.id_list) > 0:
            num = self.id_list[0]
            rv, data = self.mail.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("No messages found!")
                return

                data = data[0][1].decode('utf-8')
                msg = email.message_from_string(data)
                while msg.is_multipart():
                    msg = msg.get_payload(0)
                msgTxt = msg.get_payload(None, True).decode('utf-8')

                print("\n\n########################################")
                print("OLDEST EMAIL:")
                print(msgTxt)
                return msgTxt
        return ""


    def deleteOldestEmail(self):
        if len(self.id_list) > 0:
            num = self.id_list[0]
            self.mail.store(num, '+FLAGS', '\\Deleted')
            self.mail.expunge()


    def deleteEmail(self, emailId):
        pass

    def getMailsCount(self):
        print("emailManager : getMailsCount")
        self.__checkMail()

        if self.latest_email_id == self.first_email_id:
            if self.latest_email_id != 0:
                self.emailCount = 1
            else:
                self.emailCount = 0
        else:
            self.emailCount = self.latest_email_id - self.first_email_id

        print("Email count = " + str(self.emailCount))
        return self.emailCount
