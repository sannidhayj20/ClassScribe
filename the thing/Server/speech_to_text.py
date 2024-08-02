import speech_recognition as sr
from os import walk
file = "Server\output.wav"
r = sr.Recognizer()

def startConvertion(path = file): 
    try:
        with sr.AudioFile(path) as source:
            audio_file = r.record(source)
            output = r.recognize_google(audio_file, language='en', show_all=True)
            print("Text: {}".format(output["alternative"][0]['transcript']))
            return output["alternative"][0]['transcript']
    except TypeError:
        return "Speech not detected"
text = startConvertion()
with open("Server\output.txt", "w") as f:
    f.write(text)

def output():
    return text
