from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, os.path, time
from glob import glob

class PopMyEbooks(object):
    """docstring for PopMyEbooks."""
    def __init__(self, driver):
        self.driver = driver
        self.xpathExtendFirstBookButton = '//*[@id="product-account-list"]/div[1]/div[1]/div[3]/div[1]'
        self.xpathDownloadPdfButton = '//*[@id="product-account-list"]/div[1]/div[2]/div[2]/a[1]/div/div[3]'

    def downloadLatestBook(self):
        self.driver.find_element(By.XPATH, self.xpathExtendFirstBookButton).click()
        time.sleep(3)

        newFileList = oldFileList = self.__listFilesWithExtension('.', 'pdf')

        self.driver.find_element(By.XPATH, self.xpathDownloadPdfButton).click()
        while len(newFileList) == len(oldFileList):
            newFileList = self.__listFilesWithExtension('.', 'pdf')
            time.sleep(1)

        diffList = list(set(newFileList) - set(oldFileList))
        newFilename = diffList[0]
        fixedFilename = newFilename.lstrip('0123456789-.\\ ')
        os.rename(newFilename, fixedFilename)
        return fixedFilename

    def __listFilesWithExtension(self, dr, ext):
        return glob(os.path.join(dr,"*.{}".format(ext)))
