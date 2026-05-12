import speech_recognition as sr

# List of emergency keywords to detect
EMERGENCY_KEYWORDS = ["help", "save me", "danger", "bachao"]

def listen_for_emergency():
    """Listen to the microphone and check for emergency words."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening to the microphone. Please speak now...")
            # Adjust for ambient noise to improve recognition accuracy
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

        print("Processing your speech...")
        spoken_text = recognizer.recognize_google(audio).lower()
        print("You said:", spoken_text)

        # Check if any emergency keyword appears in the recognized text
        if any(keyword in spoken_text for keyword in EMERGENCY_KEYWORDS):
            print("EMERGENCY DETECTED")
        else:
            print("No emergency keyword detected")

    except sr.WaitTimeoutError:
        print("Microphone input timed out. Please try again.")
    except sr.UnknownValueError:
        print("Speech not understood. Please speak clearly.")
    except sr.RequestError:
        print("Could not reach Google Speech Recognition service. Check your internet connection.")
    except OSError as error:
        print("Microphone or input device error:", error)


if __name__ == "__main__":
    listen_for_emergency()
