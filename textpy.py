import time
import json
import sys

from colorama import Fore,Back
import time

def Log(string:str):
    prfx=(Fore.GREEN + time.strftime ("%H:%M:%S UTC LOG", time.localtime() )+ Back.RESET + Fore.WHITE)
    prfx = (prfx + " | ")
    log = prfx + string
    return log



def speech():
        command =""
        print(Log(" start hearing function"), flush=True)
        dataCom = {
                None:True
            }
        with open("main/command.json", 'w') as commands:
            json.dump(dataCom,commands)
        print(Log(" cleaned buffer command"), flush=True)
        status  = True
        while(status):
            command = str(input("Enter the command or question you need (use key word Virgilio): ")).lower()
            if('virgilio' in str(command)):
                print(Log(" command speech correctly "))
                data = {
                        command:False
                }
                print(Log(f" data sended - {data}"), flush=True)
                with open("main/command.json", 'w') as comandi:
                    json.dump(data, comandi,indent=4)
                if("spegniti" in command):
                    print(Log(" shutdown in progress"), flush=True)
                    status = False
            else:
                print(Log("Remember to use the key word"))
                pass
                            
        sys.exit()
                
if __name__ == "__main__":
    speech()