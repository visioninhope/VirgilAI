import sys
import json
import time
import os 

import openai
import pygame


from lib.prefix import Log
from lib.sound import create
from lib.time import now,diffTime
from lib.changeValue import change
from lib.theWeather import recoverWeather
from lib.timeConv import conversion
from lib.calendarRec import getDate,getDiff
from lib.theNews import createNews
from lib.theLight import turn
from lib.searchyt import playonyt
from lib.manageEvents import addEvents

# ---- File for manage all the preset command ----


#Start contest for GPT-3 API
messages = [
        {"role": "system", "content": "Sei un assistente virtuale chiamata Virgilio."}
    ]
current_path = os.getcwd()
file_path = os.path.join(current_path,'setting.json')

#Open file whith key api openai
with open(file_path) as f:
    secrets = json.load(f)
    _temperature= secrets['temperature']
    _max_token= secrets['max_tokens']
    api_key = secrets["openAI"]
openai.api_key = api_key


#function for communicate whith api GPT-3
def get_response(messages:list):
    print(Log(" Sto creando la risposta..."))
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = float(_temperature), # 0.0 - 2.0
        max_tokens=int(_max_token)
    )
    return response.choices[0].message

#shutdown function
def off():
    print(Log(" shut function"))
    print("\nVirgilio: Spegnimento in corso...")
    with open("connect/res.json", 'w') as file:
            data = {
                "0":["spento","spento",False]
            }
            json.dump(data,file,indent=4)
    time.sleep(2)
    sys.exit(0)
    
def Sendcommand(command:str):
    pygame.init()
    if(("spegniti" in command) or ("spegnimento" in command)):
        print(Log(" pre shut function"),flush=True)
        off()
    elif((("ore" in command) or ("ora" in command)) and (("sono" in command) or ("e'" in command))):
        print(Log(" pre time function"),flush=True)
        response = now()
        return response
    elif("stop" in command or "fermati" in command or "basta" in command):
        create("va bene mi fermo")
    elif("volume" in command and (("imposta") in command or ("metti" in command) or ("inserisci")) ):
        print(Log(" pre volume function"),flush=True)
        response = change(command)
        if(response == "104"):
            print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ")
            create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
            return None
        else:
            return response
    elif(("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command) or (("gradi" in command ) or ("temperatura" in command)) and (("quanti" in command) or ("quanta" in command))):
        print(Log(" pre wheather function"),flush=True)
        response = recoverWeather(command)
        return response
    elif("timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Log(" pre timer function"))
        try:
            command = str(command).split(" di ")[1].strip()
            my_time = conversion(command)
            return str(my_time)
        except IndexError:
            print("Please try the command again")
            create("Please try the command again")
            return None
    elif("sveglia" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Log(" pre alarm function"),flush=True)
        try:
            timeDiff = diffTime(command)
            print(timeDiff)
            my_time = conversion(timeDiff)
            print(my_time)
            return str(my_time)
        except IndexError:
            print("Please try the command again",flush=True)
            create("Please try the command again") # DA STOSTITURE COL PRESET
            return None
    elif("che giorno e" in command or "che giorno della settima e" in command):
        print(Log(" pre recovery function"),flush=True)
        response=getDate(command)
        return response
    elif("quanto mancano alle" in command or "quanto manca alle" in command):
         print(Log(" pre difftime function"),flush=True)
         response = diffTime(command)
         return response   
    elif("quanto manca al" in command or "quanti giorni mancano al" in command):
        print(Log(" pre getDiff function"),flush=True)
        response = getDiff(command)
        return response
    elif(( ("news" in command) or ("novita" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command))):
        print(Log(" pre news function"),flush=True)
        response = createNews(command)
        return response
    elif("play" in command or "riproduci" in command ):
        print(Log(" pre yt function"),flush=True)
        playonyt(command)
    elif("ricordami" in command or "imposta un promemoria" in command or "mi ricordi" in command):
        print(Log(" pre create events function"),flush=True)
        return addEvents(command)
        #TODO SEE WHAT MAKE
    elif("luce" in command and (("accendi" in command) or ("spegni" in command) )):
        print(Log(" pre light function"),flush=True)
        turn(command)
    #Question at GPT-3   
    else:
        print(Log(" GPT function"))
        messages.append({"role": "user", "content": command})
        try:
            new_message = get_response(messages=messages)
        except:
            print(Log("Unfortunately the key of openAI you entered is invalid or not present if you don't know how to get a key check the guide on github"))
            pygame.mixer.music.unload()    
            pygame.mixer.music.load('asset/ErrorOpenAi.mp3') 
            pygame.mixer.music.play()    #TO REG
        print(Log(" response created"),flush=True)
        print(f"\nVirgilio: {new_message['content']}",flush=True)
        print(Log(" I am hanging the command..."),flush=True)
        messages.append(new_message)
        print(Log(" command append"),flush=True)
        return new_message['content']
