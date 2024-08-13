import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
from decouple import config
import speech_recognition as sr
from bs4 import BeautifulSoup
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()

# Greet the user
def greet_user():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if (hour >= 0) and (hour < 12):
        speak(f"Good Morning sir")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon sir")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening sir")
    speak(f"How may I assist you?")

# Test the microphone
# def test_microphone():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Testing the microphone, please speak...")
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio, language='en-in')
#             print(f"Microphone test successful: {text}")
#         except sr.RequestError:
#             print("API was unreachable or unresponsive")
#         except sr.UnknownValueError:
#             print("Unable to recognize speech")

# Takes Input from User
def take_user_input(opt=3):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f'Listening{opt}....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print(f'Recognizing{opt}...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}')
    except sr.RequestError:
        print("API was unreachable or unresponsive")
        query = 'None'
    except sr.UnknownValueError:
        print("Unable to recognize speech")
        query = 'None'
    return query

def search_and_speak(query):
    """Perform a Google search and speak the results"""
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
        results.append(g.get_text())
        if len(results) >= 3:  # Limit to 3 results to avoid long responses
            break

    if results:
        for result in results:
            speak(result)
    else:
        speak("Sorry, I couldn't find any results for your query.")

if __name__ == '__main__':
    # test_microphone()  # Test the microphone before starting the main loop

    while True:
        query = take_user_input(1).lower()
        if 'hey jarvis' in query:
            greet_user()
            while True:
                query = take_user_input(2).lower()
                if 'open notepad' in query:
                    speak(choice(opening_text))
                    open_notepad()
                    break

                elif 'open discord' in query:
                    speak(choice(opening_text))
                    open_discord()
                    break

                elif 'open command prompt' in query or 'open cmd' in query:
                    speak(choice(opening_text))
                    open_cmd()
                    break

                elif 'open camera' in query:
                    speak(choice(opening_text))
                    open_camera()
                    break

                elif 'open calculator' in query:
                    speak(choice(opening_text))
                    open_calculator()
                    break

                elif 'ip address' in query:
                    speak(choice(opening_text))
                    ip_address = find_my_ip()
                    speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')
                    break

                elif 'wikipedia' in query:
                    speak(choice(opening_text))
                    speak('What do you want to search on Wikipedia, sir?')
                    search_query = take_user_input().lower()
                    print(search_query)
                    results = search_on_wikipedia(search_query)
                    speak(f"According to Wikipedia, {results}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(results)
                    break

                elif 'youtube' in query:
                    speak(choice(opening_text))
                    speak('What do you want to play on Youtube, sir?')
                    video = take_user_input().lower()
                    play_on_youtube(video)
                    break

                elif 'search on google' in query:
                    speak(choice(opening_text))
                    speak('What do you want to search on Google,sir?')
                    query = take_user_input().lower()
                    search_on_google(query)
                    results = search_on_wikipedia(query)
                    speak(f"here is what i found,{results}")
                    break

                elif "send whatsapp message" in query:
                    speak(choice(opening_text))
                    speak('who do you want me to text sir? ')
                    number = take_user_input().lower()
                    speak("What is the message sir?")
                    message = take_user_input().lower()
                    send_whatsapp_message(number, message)
                    speak("I've sent the message sir.")
                    break

                elif "send an email" in query:
                    speak(choice(opening_text))
                    speak("On what email address do I send sir?")
                    receiver_address = take_user_input().lower()
                    print(receiver_address)
                    speak("What should be the subject sir?")
                    subject = take_user_input().capitalize()
                    speak("What is the message sir?")
                    message = take_user_input().capitalize()
                    if send_email(receiver_address, subject, message):
                        speak("I've sent the email sir.")
                    else:
                        speak("Something went wrong while I was sending the mail. Please check the error logs sir.")
                    break

                elif 'tell me a joke' in query:
                    speak(choice(opening_text))
                    speak(f"Hope you like this one sir")
                    joke = get_random_joke()
                    speak(joke)
                    break

                elif "advice" in query:
                    speak(choice(opening_text))
                    speak(f"Here's an advice for you, sir")
                    advice = get_random_advice()
                    speak(advice)
                    speak("For your convenience, I am printing it on the screen sir.")
                    pprint(advice)
                    break

                elif 'news' in query:
                    speak(choice(opening_text))
                    speak(f"I'm reading out the latest news headlines, sir")
                    speak(get_latest_news())
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(*get_latest_news(), sep='\n')
                    break

                elif 'weather' in query:
                    speak(choice(opening_text))
                    ip_address = find_my_ip()
                    city = requests.get("https://ipapi.co/{ip_address}/city/").text
                    speak(f"Getting weather report for your city {city}")
                    weather, temperature, feels_like = get_weather_report(city)
                    speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
                    break
                
                elif 'shutdown' in query:
                    hour = datetime.now().hour
                    if hour >= 21 and hour < 6:
                        speak("Signing off, Good night sir, take care!")
                    else:
                        speak('Signing off, Have a good day sir!')
                    exit()
                    
                else:
                    speak("I'm not sure what you want, but I'll search it on Google.")
                    search_and_speak(query)

       