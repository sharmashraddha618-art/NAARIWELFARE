from flask import Flask, render_template
from jinja2 import DictLoader
import speech_recognition as sr
import geocoder
from playsound import playsound

app = Flask(__name__)

# Use a template loader with an in-memory HTML template for a beginner-friendly single file project.
app.jinja_loader = DictLoader({
    'dashboard.html': '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>NAARIWELFARE Dashboard</title>
    <style>
      body { font-family: Arial, sans-serif; background: #f7f7f7; color: #333; padding: 20px; }
      .card { background: #fff; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); padding: 20px; max-width: 600px; margin: auto; }
      h1 { color: #d6336c; }
      .row { margin-bottom: 12px; }
      .label { font-weight: bold; }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>NAARIWELFARE</h1>
      <p>Emergency status and voice detection dashboard.</p>
      <div class="row"><span class="label">Emergency Status:</span> {{ data.status }}</div>
      <div class="row"><span class="label">Detected Speech:</span> {{ data.speech }}</div>
      <div class="row"><span class="label">City:</span> {{ data.city }}</div>
      <div class="row"><span class="label">State:</span> {{ data.state }}</div>
      <div class="row"><span class="label">Country:</span> {{ data.country }}</div>
      <div class="row"><span class="label">Coordinates:</span> {{ data.coordinates }}</div>
    </div>
  </body>
</html>
'''
})

# Emergency keywords to detect in user speech.
EMERGENCY_KEYWORDS = ['help', 'save me', 'danger', 'bachao']

@app.route('/')
def home():
    """Home route for the NAARIWELFARE dashboard."""
    recognizer = sr.Recognizer()
    speech_text = 'No speech detected yet.'
    status = 'SAFE'
    city = 'Unknown'
    state = 'Unknown'
    country = 'Unknown'
    coordinates = 'Unknown'

    try:
        # Activate microphone and listen for a short voice sample.
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                speech_text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                speech_text = 'Could not understand'
            except sr.RequestError:
                speech_text = 'Speech service unavailable'
    except Exception:
        speech_text = 'Microphone not available or permission denied'

    # Check if any emergency word is present in the recognized text.
    if any(keyword in speech_text.lower() for keyword in EMERGENCY_KEYWORDS):
        status = 'EMERGENCY DETECTED'
        playsound('siren.mp3')

        try:
            # Use IP-based location detection with geocoder.
            location = geocoder.ip('me')
            if location.ok:
                city = location.city or 'Unknown'
                state = location.state or 'Unknown'
                country = location.country or 'Unknown'
                coordinates = f"{location.lat}, {location.lng}" if location.lat and location.lng else 'Unknown'
            else:
                city = state = country = coordinates = 'Location not found'
        except Exception:
            city = state = country = coordinates = 'Location error'
    elif speech_text == 'Could not understand':
        status = 'Could not understand'
    else:
        status = 'SAFE'

    # Store dashboard data in a Python dictionary.
    dashboard_data = {
        'status': status,
        'speech': speech_text,
        'city': city,
        'state': state,
        'country': country,
        'coordinates': coordinates
    }

    # Send data to the HTML template using render_template.
    return render_template('dashboard.html', data=dashboard_data)

if __name__ == '__main__':
    # Run the Flask app in debug mode for easy testing.
    app.run(host='0.0.0.0', port=5000, debug=True)
