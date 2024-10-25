import os
import requests
from datetime import datetime
from models import Alert, db

class AlertManager:
    def __init__(self):
        self.alerts = {}

    def check_thresholds(self, city, temperature, threshold=35):
        self.alerts[city] = self.alerts.get(city, 0)

        if temperature > threshold:
            self.alerts[city] += 1
            if self.alerts[city] >= 2:  # Consecutive breach trigger
                self.create_alert(city, f"Temperature exceeds {threshold}°C.")
                self.alerts[city] = 0  # Reset after alert
        else:
            self.alerts[city] = 0  # Reset if below threshold

    def create_alert(self, city, message):
        alert = Alert(city=city, message=message, timestamp=datetime.now())
        try:
            db.session.add(alert)
            db.session.commit()
        except Exception as e:
            print(f"Failed to save alert for {city}: {e}")

    def fetch_current_temperature(self, city):
        api_key = os.getenv('API_KEY')
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()['main']['temp']
        except requests.RequestException as e:
            print(f"Error fetching temperature for {city}: {e}")
            return None

    def check_alerts_for_cities(self, cities):
        for city in cities:
            temperature = self.fetch_current_temperature(city)
            if temperature:
                self.check_thresholds(city, temperature)
