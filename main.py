import speech_recognition as sr
import geocoder

EMERGENCY_KEYWORDS = ["help", "save me", "danger", "bachao"]


def get_location():
    """Fetch the current location using the public IP address."""
    try:
        location = geocoder.ip('me')
        if not location.ok:
            return None

        city = location.city or "Unknown"
        state = location.state or "Unknown"
        country = location.country or "Unknown"
        latlng = location.latlng or ["Unknown", "Unknown"]
        latitude = latlng[0]
        longitude = latlng[1]

        return {
            "city": city,
            "state": state,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
        }
    except Exception:
        return None


def print_location(location_data):
    """Print the location details in a simple format."""
    if not location_data:
        print("Could not fetch location information.")
        return

    print("Location:")
    print("  City: ", location_data["city"])
    print("  State:", location_data["state"])
    print("  Country:", location_data["country"])
    print("  Latitude:", location_data["latitude"])
    print("  Longitude:", location_data["longitude"])


def listen_for_emergency():
    """Continuously listen for emergency keywords from the microphone."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Starting microphone. Please speak clearly.")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            while True:
                print("Listening for speech...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                    print("Processing audio...")
                    text = recognizer.recognize_google(audio)
                    print("You said:", text)

                    normalized_text = text.lower()
                    if any(keyword in normalized_text for keyword in EMERGENCY_KEYWORDS):
                        print("EMERGENCY DETECTED")
                        location_data = get_location()
                        print_location(location_data)
                    else:
                        print("No emergency keyword detected")

                except sr.WaitTimeoutError:
                    print("No speech detected. Please try again.")
                except sr.UnknownValueError:
                    print("Speech was not clear enough to recognize.")
                except sr.RequestError:
                    print("Internet error: Could not connect to Google Speech Recognition.")
                except OSError:
                    print("Microphone or audio input error. Check your device.")

    except OSError:
        print("Could not access the microphone. Please check the audio device.")
    except KeyboardInterrupt:
        print("Program stopped by user.")


if __name__ == "__main__":
    listen_for_emergency()
