# importing  all requried Libraries

import pyttsx3  # this is for converting text into speech
import speech_recognition as sr  #This is for recognizing the speech and and convert it into  text
import datetime  # this is for finding exact date and time
import webbrowser   # this is for opening any thing in browser
import pywhatkit as kit #this is for  playing any thing in youtube
import requests  # this is for sending requests to the api
import subprocess  # this is for opening any System apks
import open_apps # This is a userdefined library for storing the list of web's and app's it can open
import pyautogui   # This is for keyboard shotcuts and clicking on any button or mouse related things
import time   # this is for Timer related things
import pyjokes  # this is for genreating arndome joke
import re   # this is for expressions calcultaion




# Initializing the speech engine 
engine = pyttsx3.init()




# Function to speak a text
def speak(text):   
    engine.say(text)
    engine.runAndWait()




# Function to listen for audio and recognize it then conert it into text
def listen(recognizer, prompt="Listening..."):
    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source)
            print("Finshed listening...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"Command is: {query}\n")
        except sr.WaitTimeoutError:
            print("No speech detected, trying again...") 
            return None
        except Exception as e:
            print("Jarvis is not active")
            return None
    return query.lower()




# function to fetch news  from api and tell that
def get_news():
    api_key ="99244e1416ce4878afd8fcabf51b93b5"  # this is my api key  form newsApi wbsite
    url =f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={api_key}" 
    try:
        response = requests.get(url)
        news_data= response.json()
        if news_data["status"] == "ok":
            articles = news_data["articles"][:5]
            for i , article in enumerate(articles,start=1):
                headline= article["title"]
                speak(f"Healine {i}: {headline}")
                print(f"Healine {i}: {headline}")
        else:
            speak("Sorry ! i could not tell the news right know")
            print("Failed to retrieve news. Status:", news_data["status"])
    except Exception as e:
            speak("There is  some issues while fetching the news . Sorry!")
            print(f"Error :{e}")
        



# This function is for opening websites and System apps 
def open_web_apps(app_name):
    command = open_apps.app_commands.get(app_name.lower())
    if command:
        # Check if it's a  website or a system app
        if command.startswith("http"):
            webbrowser.open(command)
            speak(f"Opening {app_name} in  browser.")
            print(f"Opening {app_name} in  browser.")
        else:
            subprocess.Popen(command, shell=True)
            speak(f"Opening {app_name}.")
            print(f"Opening {app_name}.")
    else:
        speak(f"Sorry, I don't know how to open {app_name}.")
        print(f"Unknown application or website: {app_name}")




# this function is for playing any youtube video
def play_song(video_name):
    kit.playonyt(video_name)
    speak(f"Playing {video_name} on YouTube.")
    print(f"Playing {video_name} on YouTube.")




# function to tell a randome programming joke
def tell_joke():
    joke=pyjokes.get_joke(language="en",category="neutral")
    speak(joke)
    print(joke)




# This function is for telling the spelling of word
def spelling(command):
    words = command.split()
    last_word= words[-1]
    word_spell= tuple(last_word)
    speak(f"The spelling of word {last_word} is  - {word_spell}")
    print(f"The spelling of word {last_word} is  - {word_spell}")




# this is for searching any topic on google broweser
def search_in_google(command):
    keyword = r"search for (.+)"
    match = re.search(keyword,command)
    if match:
        next_part = match.group(1)
        print(f" searching for {next_part} in google ")
        webbrowser.open(f"https://www.google.com/search?q={next_part}")
        speak(f"searching for {next_part} in google browser ")




# this function is for calculate simple calculation like 10 plus 20
def calculate_expression(expression):
    expression = expression.lower()
    expression = expression.replace("plus", "+") # in this we are replacing the word in form of oprator
    expression = expression.replace("minus", "-")
    expression = expression.replace("into", "*")
    expression = expression.replace("divided", "/")
    # Checking the expression is valid or not
    if re.match(r'^[\d+\-*/().\s]*$', expression):
        try:
            result = eval(expression)
            speak(f"The result is {result}")
            print(f"The result is {result}")
        except Exception as e:
            speak("Sorry, I couldn't calculate that.")
            print(f"Error: {e}")
    else:
        speak("I didn't understand the math expression.")
        print("Invalid expression.")

        


# this function is for extracting meaning of a word from dictionary api (This is not self written , it is an idea of chatgpt)
def get_word_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        data = response.json()
        if "title" not in data:
            meanings = data[0]['meanings'][0]['definitions']
            definition = meanings[0]['definition']
            speak(f"The meaning of {word} is: {definition}")
            print(f"The meaning of {word} is: {definition}")
        else:
            speak(f"Sorry, I couldn't find the meaning of {word}.")
            print(f"Error: Word '{word}' not found in the dictionary.")
    except Exception as e:
        speak(f"There was an error while fetching the meaning of {word}. Please try again.")
        print(f"Error: {e}")




# The main command proccesing function
def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Adjusting for background noise ...")   # think about it later
        # speak("Adjusting for background noise ...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Not active To activate, say JARVIS.")
        speak("Not active To activate, say JARVIS.")
        
        # checking if the word is wakeword then activate the assistant if not then only listen don't reply
    while True:
        command = listen(recognizer, prompt="Listening for Activation...")
        if command and "jarvis" in command:
            speak("Yes boss!")
            print("Jarvis activated!...")

            # This is for anlyzing The command and procces it
            while True:
                command = listen(recognizer)
                if command:

                    # if command is hello or hy then spaek hello or hy
                    if "hy" in command or "hello" in command:
                        speak("Hi Rk sir, how can I assist you?")

                    
                    #if command id open google or camera etc. ,then open it
                    elif   "open" in command:
                        app_name = command.replace("open ", "").strip()  # Extracts the app name
                        open_web_apps(app_name)

                    
                    # this is the going previous tab 
                    elif "previous" in command:
                        speak("Going back to the previous application.")
                        print("Switching to the previous application.")
                        pyautogui.hotkey("alt", "tab")
                        time.sleep(1)


                    # this is for opening taskbar with a command like - open taskbar
                    elif "taskbar" in command:
                        speak("opening taskbar")
                        pyautogui.hotkey("super","a") 
                        print("opening taskbar")
                    

                    #This command will select all texts if cursior is in text location
                    elif "select all" in command :
                        pyautogui.hotkey("ctrl","a")
                        print("text is selected")
                        speak("text is selected")


                    # this is for coping the selected text
                    elif "copy" in command:
                        pyautogui.hotkey("ctrl","c")
                        print("text is copied")
                        speak("text is copied")
                    

                    # this is for paste the copied text
                    elif "paste" in command:
                        pyautogui.hotkey("ctrl","v")
                        print("text is pasted")
                        speak("Text is pasted")

                    
                    #Tell the spelling of  a word with command like - tell the spelling of ddog
                    elif "spelling" in command:
                        spelling(command)

                    
                    #Tell the meaning of a word with command like - tell the meaning of word
                    elif "meaning of" in command:
                        words = command.split()
                        last_word = words[-1]
                        get_word_meaning(last_word)

                    
                    #if command is calculate (expression) then it is tell the answer of it
                    elif "calculate" in command or "solve" in command:
                        expression = command.replace("calculate", "").replace("solve", "").strip()
                        calculate_expression(expression)


                    #this is for pressing windows button
                    elif "windows" in command:
                        pyautogui.press('super')


                    #This is for taking a screenshot
                    elif "screenshot" in command:
                        pyautogui.hotkey("super","prtsc")
                        print("screenshot taked")                                   
                        speak("screenshot taked") 


                    #This is for play any video on youtube
                    elif "play" in command:
                        video_name = command.replace("play", "").strip()
                        play_song(video_name)

                    
                    #This is for serching any topic on google
                    elif "search for" in command:
                        search_in_google(command)


                    #this is a wait command to wait for some times
                    elif "wait" in command:
                        speak("Yes! I am waiting for your command.")


                    # It tells the current time
                    elif "the time" in command:
                        str_time = datetime.datetime.now().strftime("%H:%M")
                        speak(f"The time is now {str_time}")

                    #it tells the today's date
                    elif "date" in command:
                        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
                        speak(f"Today is {today}")
                        print(f"Today is {today}")


                    #It tell the top 5 news headline
                    elif "news" in command:
                        print("Fetching news...")
                        speak("Fetching latest news !! ")
                        get_news()
                        speak("Yes ! these are the top 5 news headlines")


                    #it tells a randome joke
                    elif "joke" in command:
                        speak("Here is Joke for you")
                        tell_joke()


                    #tells the name
                    elif "name" in command:
                        speak("My name is Jarvis and , i am your lovely voice assistant")
                        print("My name is Jarvis and , i am your lovely voice assistant")
                    


                    # it tells a motivation quote which is predefined (we can connect it with a api )
                    elif "motivation" in command:
                        print("Nothing is impossible. Even if ,The word itself says 'I'm possible! . So  you can do anything")
                        speak("Nothing is impossible. Even is , The word itself says 'I'm possible!. so you can do anything")


                    # if  user says thank you then it is for welcome it
                    elif "thank" in command:
                        print("Your welcome !")
                        speak("Your welcome!")
                        return



                    # this is for terminating the programm
                    elif "stop" in command or "exit" in command:
                        speak("Terminating the program and exiting successfully.")
                        return  # Exiting the program

                    
                    # if command is not in these commands
                    else:
                        speak("I did not understand what you said.")


                # if command is empty then deactivate the jarvis       
                else:
                    speak("jarvis is deactivated")
                    print("Jarvis is deactivated")
                    break
                

# calling the main function
main()

# End of the program
