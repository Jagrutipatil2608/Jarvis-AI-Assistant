import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
       
    prompt = f"""
You are Jarvis, a helpful virtual assistant.

Answer this question:
User : {command}
"""

    response = client.models.generate_content (
         model="gemini-2.5-flash",
         contents = prompt
   
   )

    return response.text
 


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com") 
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "").strip() 
        link = musicLibrary.music[song]
        webbrowser.open(link) 

    else:
        #    let open ai handle the request
        output = aiprocess(c)
        speak(output)
        pass

        
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        #Listen for wake word "Jarvis"
        #obtain audioi for microphone
        r = sr.Recognizer()

        
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
             print("Listening..")
             audio = r.listen(source, timeout = 2,phrase_time_limit = 2)
            command =   r.recognize_google(audio)
            if "jarvis" in command.lower():
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Listening..")
                    audio = r.listen(source)
                    command =   r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))