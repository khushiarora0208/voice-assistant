import speech_recognition as sr
import pyttsx3
import ollama

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Increase speed
    engine.setProperty('volume', 1.0)  # Set max volume
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return ""

def ask_ollama(prompt):
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}], options={'max_tokens': 100})
    return response['message']['content']


def main():
    speak("Hello, how can I assist you?")
    while True:
        command = listen()
        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        if command:
            response = ask_ollama(command)
            print("Assistant:", response)
            speak(response)

if __name__ == "__main__":
    main()
