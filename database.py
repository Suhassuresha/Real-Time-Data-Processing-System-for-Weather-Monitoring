import os
import sqlite3
from .models import db, AlertThreshold, Alert
from datetime import datetime

def connect_db():
    # Get the database path from the environment variable
    db_path = os.getenv('DATABASE_URL', os.path.join(os.path.abspath(os.path.dirname(__file__)), 'realdata.db'))
    
    # Normalize the database URL for SQLite
    if db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "")  # Remove the sqlite:// prefix for the connect function

    print(f"Database path: {db_path}")  # Debugging line
    return sqlite3.connect(db_path)

def get_daily_summary():
    query = '''
        SELECT city, date, AVG(avg_temp) as average_temp, MAX(max_temp) as max_temp,
               MIN(min_temp) as min_temp, condition
        FROM weather_summary
        WHERE date = CURRENT_DATE
        GROUP BY city, date;
    '''
    return execute_query(query)

def get_weather_trends():
    query = 'SELECT city, avg_temp, trend_date FROM weather_trends'
    return execute_query(query)

def execute_query(query):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []

def check_alert_thresholds(city, temp, condition):
    # Fetch the user-defined threshold for this city
    threshold = AlertThreshold.query.filter_by(city=city).first()

    if threshold:
        if temp > threshold.temp_threshold:
            trigger_alert(city, temp, condition)

def trigger_alert(city, temp, condition):
    alert_message = f"Alert for {city}: Temperature {temp}°C exceeds the threshold!"
    print(alert_message)

    # Save this alert in the database for frontend display
    alert = Alert(city=city, message=alert_message, date=datetime.now())
    db.session.add(alert)
    db.session.commit()