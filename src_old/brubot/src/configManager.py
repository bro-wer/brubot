import os
import sqlite3

class configManager():
    """Class used to read/save data in local database"""

    def __init__(self, dbName):
        print("Starting configManager...")
        self.BASENAME = dbName
        self.STARTDIR = str(os.getcwd())
        self.BASEPATH = os.path.join(self.STARTDIR, self.BASENAME)

        self.dbTables = {
                         "mainTable" : "Used to store main credentials",
                         # "todoTable" : "Used to jobs to be done",
                         # "doneTable" : "Used to store done jobs",
                         }
        self.dbTableFields = {
                        "mainTable" : ["name", "value"],
                        #"todoTable" : ["name?", "status", "actionName"],
                        }
        self.__initDbManager()

    def __initDbManager(self):
        self.dbManager = dbManager(dbName = self.BASENAME)
        for tableName, tableFields in self.dbTableFields.items():
            self.dbManager.initTable(tableName, tableFields)

    def start(self):
        print("Starting configManager...")

    def close(self):
        self.dbManager.close()

    def getEmailUser(self):
        record = self.dbManager.getRow("mainTable", "({})".format("name='emailUser'"))
        value = record[self.dbTableFields["mainTable"].index("value")]
        return value

    def setEmailUser(self, newEmailUser):
        self.dbManager.deleteRow("mainTable", "({})".format("name='emailUser'"))
        self.dbManager.insertRow("mainTable", "('{}','{}')".format('emailUser', newEmailUser))

    def getEmailPass(self):
        record = self.dbManager.getRow("mainTable", "({})".format("name='emailPass'"))
        value = record[self.dbTableFields["mainTable"].index("value")]
        return value

    def setEmailPass(self, newEmailPass):
        self.dbManager.deleteRow("mainTable", "({})".format("name='emailPass'"))
        self.dbManager.insertRow("mainTable", "('{}','{}')".format('emailPass', newEmailPass))

    def getMainTable(self):
        tableName = "mainTable" 
        mainTable = self.dbManager.getTable(tableName)
        print("\t".join(self.dbTableFields[tableName]))
        for row in mainTable:
            print("\t".join(row))



class dbManager():
    """ Helper class used to simplify all db related actions."""
    def __init__(self, dbName):
        self.dbName = dbName
        self.dbConn = sqlite3.connect(self.dbName)
        self.dbCursor = self.dbConn.cursor()

    def close(self):
        self.dbConn.close()

    def checkIfTableExists(self, tableName):
        print("dbManager: checkIfTableExists")
        self.dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName))
        try:
            if len(self.dbCursor.fetchone()) > 0:
                return True
        except Exception as e:
            return False

    def getTable(self, tableName):
        print(type(self.dbCursor.execute("SELECT * FROM {}".format(tableName))))
        resultList = []
        for row in self.dbCursor.execute("SELECT * FROM {}".format(tableName)):
            print(row)
            resultList.append(row)
        return resultList


    def createTable(self, tableName, tableFields):
        self.dbCursor.execute("CREATE TABLE {} ({})".format(tableName, ','.join(map(str, tableFields))))
        self.dbConn.commit()

    def deleteTable(self, tableName):
        print("dbManager: deleteTable")

    def getRow(self, tableName, whereCondition):
        self.dbCursor.execute("SELECT * FROM {} WHERE {}".format(tableName, whereCondition))
        try:
            response = self.dbCursor.fetchone()
            return response
        except Exception as e:
            print("Failed to obtain row from {} table with the conditionfollowing condition:\n{}".format(tableName, whereCondition))
            print(str(e))
            return {"":""}

    def insertRow(self, tableName, rowData):
        self.dbCursor.execute("INSERT INTO {} VALUES {}".format(tableName, rowData))
        self.dbConn.commit()

    def deleteRow(self, tableName, whereCondition):
        self.dbCursor.execute("DELETE FROM {} WHERE {}".format(tableName, whereCondition))
        self.dbConn.commit()

    def initTable(self, tableName, tableFields):
        if self.checkIfTableExists(tableName):
            #TODO: add comparison for table fields and notify user if these are the same as the requested ones
            print("Requested table already exists: " + tableName)
        else:
            self.createTable(tableName, tableFields)

if __name__ == '__main__':
    tempManager = configManager('example.db')

    while True:
        print("What do you want to do?")
        print("\t0 - Print main table")
        print("\t1 - Update email account")
        print("\tq - Exit")
        choice = str(input("What's your choice? "))
        if choice == "0":
            tempManager.getMainTable()
        elif choice == "1":
            email = str(input("What's new email? "))
            pass1 = str(input("What's new pass? "))
            pass2 = str(input("Please confirm pass: "))
            while pass1 != pass2:
                print("Provided passwords do not match!")
                pass1 = str(input("What's new pass? "))
                pass2 = str(input("Please confirm pass. "))
            tempManager.setEmailUser(email)
            tempManager.setEmailPass(pass1)
            print("New email: " + tempManager.getEmailUser())
            print("New pass: " + tempManager.getEmailPass())

        else:
            print("Goodbye")
            tempManager.close()
            break
