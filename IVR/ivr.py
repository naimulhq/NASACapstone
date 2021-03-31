import speech_recognition as sr
import time
from time import ctime
import webbrowser
import os
import playsound
import random
from gtts import gTTS
import pyttsx3
#import mpg123
# engine=pyttsx3.init()
# engine.setProperty('rate',150)
# engine.setProperty('voice','english+m2')
r = sr.Recognizer()

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            argo_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnkownValueError:
            print("Sorry, I did not get that")
        except sr.RequestError:
            print("Sorry, my speech service is down")

        # voice_data = r.recognize_google(audio)
        print(voice_data)
    return voice_data

def argo_speak(audio_string):
    tts =gTTS(text=audio_string, lang='en')
    ran = random.randint(1,10000000)
    audio_file = 'audio-' +str(ran) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

# def argo_speak(audio_string):
#     engine.say(audio_string)
#     print(audio_string)

# def argo_speak(audio_string):
#     output =gTTS(text=audio_string, lang='en',slow=False)
#     output.save('output.mp3')
#     print(audio_string)
#     os.system('mpg123 output.mp3')

def respond(voice_data):
    if 'what is your name' in voice_data:
        argo_speak('My name is Argo')
        
    if 'what time is it' in voice_data:
        argo_speak(ctime())

    if 'search' in voice_data:
        search = record_audio('What do you want to search for')
        url = 'https:/google.com/search?q=' + search
        webbrowser.get().open(url)
        argo_speak('Here is what I found for ' + search)

    if 'find location' in voice_data:
        location = record_audio('What is the location')
        url = 'https:/google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        argo_speak('Here is the location of ' + location)

    if 'exit' in voice_data:
        argo_speak('Good bye')
        exit()

time.sleep(1)
argo_speak('How can i help') 


while 1:
    voice_data = record_audio()
    respond(voice_data)
    #engine.runAndWait()