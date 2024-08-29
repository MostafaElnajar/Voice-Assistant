import speech_recognition as sr
from gtts import gTTS
import winsound
from pydub import AudioSegment
import pyautogui
import webbrowser
import pycurl
from io import BytesIO

# Listen for voice commands
def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

# Respond to the user
def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)
    # os.system("afplay response.mp3") for non-windows

# Send HTTP request using pycurl
def send_http_request(url, data, auth_token):
    response = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.setopt(c.HTTPHEADER, [
        f"Authorization: Bearer {auth_token}",
        "Content-Type: application/json"
    ])
    c.setopt(c.POSTFIELDS, data)
    c.perform()
    c.close()
    return response.getvalue().decode('utf-8')


def send_http_requestACon(url, dataACon, auth_token):
    response = BytesIO()
    c1 = pycurl.Curl()
    c1.setopt(c1.URL, url)
    c1.setopt(c1.WRITEFUNCTION, response.write)
    c1.setopt(c1.HTTPHEADER, [
        f"Authorization: Bearer {auth_token}",
        "Content-Type: application/json"
    ])
    c1.setopt(c1.POSTFIELDS, dataACon)
    c1.perform()
    c1.close()
    return response.getvalue().decode('utf-8')

def send_http_requestACoff(url, dataACoff, auth_token):
    response = BytesIO()
    c2 = pycurl.Curl()
    c2.setopt(c2.URL, url)
    c2.setopt(c2.WRITEFUNCTION, response.write)
    c2.setopt(c2.HTTPHEADER, [
        f"Authorization: Bearer {auth_token}",
        "Content-Type: application/json"
    ])
    c2.setopt(c2.POSTFIELDS, dataACoff)
    c2.perform()
    c2.close()
    return response.getvalue().decode('utf-8')
tasks = []
listeningToTask = False


lightsON = ["turn on lights","turn on the lights","turn on light" ,"turn on the light","turn lights on","turn the lights on","turn light on","turn the light on","lights on", "lights turn on", "light turn on", "open the lights","open lights", "open light", "open the light"]
lightsOFF = ["turn off lights","turn off the lights","turn off light" ,"turn off the light","turn lights off","turn the lights off","turn light off","turn the light off","lights off", "lights turn off", "light turn off", "close the lights","close lights", "close light", "close the light"]
acON = ["turn on ac","turn on the ac","turn ac on","turn the ac on","ac on", "ac turn on", "the ac turn on", "open the ac", "open ac"]
acOFF = ["turn off ac","turn off the ac","turn ac off","turn the ac off","ac off", "ac turn off", "the ac turn off", "close the ac", "close ac"]


def main():
    global tasks
    global listeningToTask
    
    auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkN2E0ZDAxMDkxZjg0YWU3OTU0NzY4MmE0YzE5YWZmZiIsImlhdCI6MTcyNDI0MTA1NSwiZXhwIjoyMDM5NjAxMDU1fQ.DRVssTbI6TV-fYjQG_gC6U1bE6hhyWKSqOdzolbSbhA"
    on_url = "http://172.19.113.2:8123/api/services/switch/turn_on"
    off_url = "http://172.19.113.2:8123/api/services/switch/turn_off"
    data = '{"entity_id": "switch.test_light_1"}'
    dataACoff = '{"entity_id": "switch.ac_off"}'
    dataACon = '{"entity_id": "switch.20"}'
    while True:
        print("Waiting for the wake-up word 'ameca'...")
        command = listen_for_command()

        if command and "ameca" in command:
            respond("Yes, how can I assist you?")
            command = listen_for_command()

            if command:
                if listeningToTask:
                    tasks.append(command)
                    listeningToTask = False
                    respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
                elif "add a task" in command:
                    listeningToTask = True
                    respond("Sure, what is the task?")
                elif "list tasks" in command:
                    respond("Sure. Your tasks are:")
                    for task in tasks:
                        respond(task)

                elif "open chrome" in command:
                    respond("Opening Chrome.")
                    webbrowser.open("https://www.google.com")

                elif any(phrase in command for phrase in lightsON):
                    result = send_http_request(on_url, data, auth_token)
                    respond("Lights turned on.")

                elif any(phrase in command for phrase in lightsOFF):
                    result = send_http_request(off_url, data, auth_token)
                    respond(f"lights turned off.")
                
                elif any(phrase in command for phrase in acON):
                    result = send_http_requestACon(on_url, dataACon, auth_token)
                    respond(f"ac turned on.")

                elif any(phrase in command for phrase in acOFF):
                   result = send_http_requestACoff(on_url, dataACoff, auth_token)
                   respond(f"ac turned off.")



                elif "thanks" in command:
                    respond("Goodbye!")
                    break
                else:
                    respond("Sorry, I'm not sure how to handle that command.")

if __name__ == "__main__":
    main()
