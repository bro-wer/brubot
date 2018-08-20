import json, os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .popNewEbookPage import PopNewEbookPage
from .popMyEbooks import PopMyEbooks

class PacktHub(object):
    """
    Class used to handle all automatic duties related with obtaining free books from packtub.
    """

    def __init__(self):
        self.ownedBooksJsonPath = os.path.join('settings', 'ownedBooks.json')
        self.configJsonPath = os.path.join('settings', 'packthub.json')

        with open(self.configJsonPath) as f:
            self.configJson = json.load(f)
        self.resultMessage = "Packthub job status:\n"
        self.__initSelenium()
        self.__obtainOwnedBooksList()

    def __initSelenium(self):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : os.getcwd()}
        chromeOptions.add_experimental_option("prefs",prefs)

        self.driver = webdriver.Chrome(executable_path = os.path.join(os.getcwd(), 'src', 'packthub', 'tools', 'chromedriver.exe'), chrome_options=chromeOptions)
        self.newEbookPage = PopNewEbookPage(driver = self.driver)
        self.popMyEbooks = PopMyEbooks(driver = self.driver)

    def __obtainOwnedBooksList(self):
        with open(self.ownedBooksJsonPath) as f:
            self.ownedBooksList = json.load(f)

    def finishSelenium(self):
        self.driver.close()

    def getStatus(self):
        print(self.resultMessage)
        return self.resultMessage

    def runJob(self):
        print("PacktHub : runJob")
        try:
            self.__checkNewBook()
        except Exception as e:
            raise
        finally:
            self.finishSelenium()

    def __checkNewBook(self):
        try:
            self.driver.get(self.configJson["freeEbookUrl"])
            self.newEbookName = self.driver.find_element(By.XPATH, self.newEbookPage.xpathNewEbook).text
            self.resultMessage += "New ebook name: {}\n".format(self.newEbookName)
            self.__checkIfEbookAlreadyOwned()
        except Exception as e:
            self.resultMessage += "Failed to obtain new ebook name.\n"
            raise

    def __checkIfEbookAlreadyOwned(self):
        if self.newEbookName in self.ownedBooksList:
            self.resultMessage += "This book is already owned.\n"
        else:
            self.downloadEbook()


    def downloadEbook(self):
        print("PacktHub : downloadEbook")
        try:
            self.newEbookPage.login(username = self.configJson["username"],
                                    userpass = self.configJson["userpass"])
            self.driver.get(self.configJson["myEbooksUrl"])
            self.newPdfName = self.popMyEbooks.downloadLatestBook()
            self.resultMessage += "New ebook has been downloaded as: {}\n".format(self.newPdfName)
            self.updateOwnedBooksList()
            os.remove(self.newPdfName)
        except Exception as e:
            self.resultMessage += "Failed to download new ebook name.\n"
            raise

    def updateOwnedBooksList(self):
        self.ownedBooksList.append(self.newEbookName)
        with open(self.ownedBooksJsonPath, 'w') as outfile:
            json.dump(self.ownedBooksList, outfile)
