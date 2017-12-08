#!/usr/bin/python

import time
import csv
from pexpect import pxssh


#print banner
intro_screen = """
   ___                                    _     ___ _
  / _ \__ _ ___ _____      _____  _ __ __| |   / __\ |__   __ _ _ __   __ _  ___ _ __
 / /_)/ _` / __/ __\ \ /\ / / _ \| '__/ _` |  / /  | '_ \ / _` | '_ \ / _` |/ _ \ '__|
/ ___/ (_| \__ \__ \\ V  V / (_) | | | (_| | / /___| | | | (_| | | | | (_| |  __/ |
\/    \__,_|___/___/ \_/\_/ \___/|_|  \__,_| \____/|_| |_|\__,_|_| |_|\__, |\___|_|
                                                                      |___/
\n
This should only be used when there are multiple devices to make changes to:
    1 - Upload CSV of device IPs
    2 - State common username among devices
    3 - State Current password of devices
    4 - Set new password for devices
                                                                                        """


#engine to run application
class Engine(object):
    def __init__(self, intro_screen):
        self.intro_screen = intro_screen
    def run(self):
        print self.intro_screen
        gatherInfo()
        executeChange(csvFile)


def gatherInfo():
    global csvFile
    global username
    global oldPW
    global newPW
    global s

    csvFile = raw_input("CSV file> ")
    username = raw_input("Username> ")
    oldPW = raw_input("Current password> ")
    newPW = raw_input("New password> ")
    doublecheckPW = raw_input("Re-type New password> ")
    while newPW != doublecheckPW:
        print "Passwords do not match!"
        newPW = raw_input("New password> ")
        doublecheckPW = raw_input("Re-type New password> ")
    else:
        print "\nConnecting..."



#define function to connect to telepresence device via ssh, sets up hostname and login credentials
def connectTPD(s, endpointIP, username, oldPW):
    s.force_password = True
    s.PROMPT = 'SSH>'
    s.login(endpointIP, username, oldPW, auto_prompt_reset = False)
    s.prompt()

def executeChange(csvFile):
    print "Making Changes..."
    with open(csvFile) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            endpointIP = row[0]
            s = pxssh.pxssh(timeout=1, maxread=2000000)
            connectTPD(s, endpointIP, username, oldPW)
            s.sendline("systemtools passwd")
            s.prompt()
            data = s.before
            time.sleep(15)
            print data
            time.sleep(5)
            s.sendline("")
            s.prompt()
            data = s.before
            time.sleep(15)
            print data
            time.sleep(5)
            s.sendline(new_pass)
            s.prompt()
            data = s.before
            time.sleep(15)
            print data
            time.sleep(5)
            s.sendline(new_pass)
            s.primpt()
            data = s.before
            time.sleep(15)
            print data
            s.sendline("bye")
            s.logout()
            s.close()
            s = "0"




a_script = Engine(intro_screen)
a_script.run()
