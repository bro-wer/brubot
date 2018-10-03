# global imports
import datetime
import os
from os.path import getmtime
import psutil
import sys
import time
import subprocess
import sqlite3


class ScriptServer():
    """docstring for ScriptServer """

    def __init__(self):
        self.STARTDIR = str(os.getcwd())
        self.SRCDIR = os.path.join(self.STARTDIR, 'src')
        self.BRUBOTPATH = os.path.join(self.SRCDIR, 'brubot.py')
        self.BRUBOTEXEC = ["python3", self.BRUBOTPATH]
        self.CONFIGPATH = os.path.join(self.STARTDIR, 'config.db')
        self.__initGlobals()

    def __initGlobals(self):
        self.WATCHED_FILES = []
        self.WATCHED_FILES_MTIMES = []

        for root, subFolders, files in os.walk(self.SRCDIR):
            for file in files:
                self.WATCHED_FILES.append(os.path.join(root, file))
        self.WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in self.WATCHED_FILES]

    def checkIfSourcesChanged(self):
        for f, mtime in self.WATCHED_FILES_MTIMES:
            if getmtime(f) != mtime:
                self.brubotReset()
                return True
        return False

    def brubotStart(self):
        self.brubotProcess = subprocess.Popen(self.BRUBOTEXEC)

    def brubotKill(self):
        # os.killpg(os.getpgid(self.brubotProcess.pid), signal.SIGTERM)
        psutil.Process(self.brubotProcess.pid).terminate()

    def brubotReset(self):
        print("Restarting server...")
        self.brubotKill()
        self.__initGlobals()
        self.brubotStart()

if __name__ == '__main__':
    print("Starting server...")
    os.chdir("/home/pi/Workspace/brubot")
    server = ScriptServer()
    server.brubotStart()


    with open('log.txt', 'a') as f:
        f.write("Another test: " + str(datetime.datetime.now()) + "\n")

    while True:
        time.sleep(5)
        server.checkIfSourcesChanged()
