from flask import Flask, render_template
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

app = Flask(__name__)

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change the voice index

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I am your voice assistant. How can I help you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not hear your request. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def open_browser(url):
    webbrowser.open(url)

def open_photo():
    photo_path = "C:/Program Files/Python311/Scripts/pythonlib"  # Update the path to your photo directory
    os.startfile(photo_path)

def process_command():
    query = take_command()

    if query:
        # Logic for executing tasks based on user's command
        if 'wikipedia' in query.lower():
            speak("Searching Wikipedia...")
            query = query.replace("Wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            print(results)
            speak(results)
            return results
        elif 'open YouTube' in query.lower():
            open_browser("https://www.youtube.com")
            return "Opening YouTube..."
        elif 'open Google' in query.lower():
            open_browser("https://www.google.com")
            return "Opening Google..."
        elif 'open stack overflow' in query:
            open_browser("https://stackoverflow.com")
            return "Opening Stack Overflow..."
        elif 'open facebook' in query:
            open_browser("https://www.facebook.com")
            return "Opening Facebook..."
        elif 'open whatsapp' in query:
            open_browser("https://web.whatsapp.com")
            return "Opening WhatsApp..."
        elif 'time' in query.lower():
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
            return f"The current time is {current_time}"
        elif 'exit' in query.lower() or 'bye' in query.lower():
            speak("Goodbye!")
            return "Goodbye!"
        elif 'open photo' in query:
            open_photo()
            return "Opening photos..."
        else:
            speak("I'm sorry, I didn't understand that command. Can you please repeat?")
            return "I'm sorry, I didn't understand that command. Can you please repeat?"
    return None

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process_command')
def process_command_route():
    result = process_command()
    return render_template('result.html', result=result)

if __name__ == '__main__':
    wish_me()
    app.run(debug=True)
