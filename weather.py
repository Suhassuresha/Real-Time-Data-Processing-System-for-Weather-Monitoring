import os
import requests
from datetime import datetime
from collections import Counter
from .models import WeatherSummary, db, DailySummary, AlertThreshold, Alert
from flask import current_app
import time
import logging

API_KEY = os.getenv('API_KEY')
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_and_summarize_weather_data():
    with current_app.app_context():  # Push the app context
        summaries = []
        for city in CITIES:
            try:
                response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
                response.raise_for_status()  # Will raise an error for bad responses
                
                data = response.json()

                # Ensure the API returned the expected data structure
                if 'main' in data and 'weather' in data and 'wind' in data:
                    # Check if an entry for today already exists
                    existing_entry = WeatherSummary.query.filter_by(city=city, date=datetime.now().date()).first()
                    if existing_entry:
                        # Update the existing entry
                        existing_entry.avg_temp = data['main']['temp']
                        existing_entry.max_temp = data['main']['temp_max']
                        existing_entry.min_temp = data['main']['temp_min']
                        existing_entry.condition = data['weather'][0]['description']
                        existing_entry.humidity = data['main']['humidity']  # New line for humidity
                        existing_entry.wind_speed = data['wind']['speed']  # New line for wind speed
                    else:
                        # Create a new entry
                        weather_entry = WeatherSummary(
                            city=city,
                            date=datetime.now().date(),
                            avg_temp=data['main']['temp'],
                            max_temp=data['main']['temp_max'],
                            min_temp=data['main']['temp_min'],
                            condition=data['weather'][0]['description'],
                            humidity=data['main']['humidity'],  # New line for humidity
                            wind_speed=data['wind']['speed']  # New line for wind speed
                        )
                        db.session.add(weather_entry)

                    summaries.append({
                        'city': city,
                        'temperature': data['main']['temp'],
                        'feels_like': data['main']['feels_like'],
                        'condition': data['weather'][0]['description'],
                        'humidity': data['main']['humidity'],  # New line for humidity
                        'wind_speed': data['wind']['speed']  # New line for wind speed
                    })
                else:
                    logging.error(f"Unexpected data structure for city {city}: {data}")
            except requests.RequestException as req_err:
                logging.error(f"Request error for {city}: {req_err}")
            except Exception as e:
                logging.error(f"Error fetching data for {city}: {e}")

        try:
            db.session.commit()
        except Exception as commit_err:
            logging.error(f"Database commit error: {commit_err}")
            db.session.rollback()  # Rollback if there's an error

    return summaries


def calculate_daily_aggregates():
    today = datetime.now().date()
    today_weather = WeatherSummary.query.filter_by(date=today).all()

    if not today_weather:
        logging.info("No weather data available for today.")
        return []

    daily_summary = []

    for city in CITIES:
        city_weather = [entry for entry in today_weather if entry.city == city]
        if city_weather:
            avg_temp = sum(entry.avg_temp for entry in city_weather) / len(city_weather)
            max_temp = max(entry.max_temp for entry in city_weather)
            min_temp = min(entry.min_temp for entry in city_weather)

            # Get the dominant weather condition
            condition_counter = Counter(entry.condition for entry in city_weather)
            dominant_condition = condition_counter.most_common(1)[0][0]

            daily_summary.append({
                'city': city,
                'date': today,
                'average_temperature': avg_temp,
                'max_temperature': max_temp,
                'min_temperature': min_temp,
                'dominant_condition': dominant_condition,
            })

            # Store this daily summary into the DB
            db.session.add(DailySummary(city=city, date=today, avg_temp=avg_temp, 
                                         max_temp=max_temp, min_temp=min_temp, 
                                         condition=dominant_condition))

    db.session.commit()
    return daily_summary


def schedule_weather_fetching(app):
    with app.app_context():  # Create the app context here
        while True:
            fetch_and_summarize_weather_data()
            time.sleep(int(os.getenv('FETCH_INTERVAL', 300)))  # Convert minutes to seconds

def check_alerts(city, weather_data):
    threshold = AlertThreshold.query.filter_by(city=city).first()
    alerts_triggered = []

    if threshold:
        if weather_data['temperature'] > threshold.max_temp:
            alert_message = f"Temperature in {city} exceeds {threshold.max_temp}°C! Current temperature: {weather_data['temperature']}°C"
            trigger_alert(city, alert_message)
            alerts_triggered.append(alert_message)

        if threshold.condition and threshold.condition.lower() in weather_data['condition'].lower():
            alert_message = f"Weather condition alert in {city}: {weather_data['condition']}"
            trigger_alert(city, alert_message)
            alerts_triggered.append(alert_message)

    return alerts_triggered

def trigger_alert(city, message):
    new_alert = Alert(city=city, message=message)
    db.session.add(new_alert)
    db.session.commit()
