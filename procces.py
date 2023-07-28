import json
import sys
import time
import os
import threading
import calendar
import datetime
import threading

import requests
import openai
from colorama import Fore, Back
import speech_recognition as sr

from lib.prefix import Log
from lib.chooseCommand import Sendcommand
from lib.request import getEvents


# init the recognizer
listener = sr.Recognizer()

with open('setting.json') as f:
    setting = json.load(f)
    listener.operation_timeout = int(setting['operation_timeout'])
    listener.dynamic_energy_threshold = bool(setting['dynamic_energy_threshold'])
    listener.energy_threshold = int(setting['energy_threshold'])
    
    wordActivation = str(setting['wordActivation']).lower()

def update_json_value(key, new_value):
    # Apri il file JSON e carica i dati
    with open("connect/command.json", 'r') as file:
        data = json.load(file)
    # Modifica il valore desiderato
    if key in data:
        data[key] = new_value
    else:
        print(Log(f"The key '{key}' dont exist in the file JSON."), flush=True)
    # Sovrascrivi il file JSON con i dati aggiornati
    with open("connect/command.json", 'w') as file:
        json.dump(data, file, indent=4)


def cleanCommand(command):
    # Cancellation element before the key word
    try:
        command = str(command).split(f"{wordActivation} ")[1].strip()
        print(Log(f" command processed: {command} "), flush=True)
        return command
    except IndexError:
        #If command contain only virgil word
        return command


def send(command: str):
    command = cleanCommand(command)
    print(Log(" command heard correctly"), flush=True)
    print(Log(" command in process"), flush=True)
    res = Sendcommand(command)
    print(Log(" command processed updating file with the result"), flush=True)
    with open("connect/res.json", 'w') as file:
        data = {
            "0": [command, res, False]
        }
        json.dump(data, file, indent=4)


def cleanBuffer():
    dataRes = {
        "0": [None, None, True]
    }
    with open("connect/res.json", 'w') as res:
        json.dump(dataRes, res)
    print(Log(" cleaned buffer result"), flush=True)

def checkEvent():
    with open("connect/reminder.txt","w") as f:
        f.write("0")
    time.sleep(86400)   
    #parte allarme
    
class EventThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
    def run(self):
           checkEvent() 

def main():
    print(Log(Fore.GREEN + " THE ASSISTENT IS ONLINE  "), flush=True)
    cleanBuffer()
    print(Log(" Start check event"), flush=True)
    t = EventThread()
    t.start()
    while (True):
        with open("connect/command.json", 'r') as commands:
            command = commands.read()
            if ("spegniti" in command):
                commandToElaborate = "virgilio spegniti"
            else:
                commandToElaborate = "".join(command.split(":")[0])[7:-1]
        if ("false" in command and command != None):
            print(Log(f" command processed: {commandToElaborate}"), flush=True)
            #TODO VERIFY IF WIHOUT THIS THE CODE WORK
            send(commandToElaborate)
            print(Log(f" updating the command"), flush=True)
            update_json_value(commandToElaborate, True)
        else:
            pass


if __name__ == "__main__":
    main()
