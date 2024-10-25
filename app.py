import os 
from flask import Flask, render_template, jsonify
from .weather import fetch_and_summarize_weather_data, schedule_weather_fetching, calculate_daily_aggregates
from .database import get_daily_summary, get_weather_trends
from .config import load_config
from .models import db, Alert
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import logging
import threading
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
base_dir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the current directory
app = Flask(__name__,
            static_folder=os.path.join(base_dir, '../frontend/static'),
            template_folder=os.path.join(base_dir, '../frontend/templates'))

# Load config from environment or config file
config = load_config()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', config['db_path'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Start a background thread for fetching weather data
threading.Thread(target=schedule_weather_fetching, args=(app,), daemon=True).start()
# Start the thread here

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather_summary', methods=['GET'])
def weather_summary():
    try:
        summary = fetch_and_summarize_weather_data()
        return jsonify(summary), 200
    except Exception as e:
        logging.error(f"Error fetching weather summary: {e}")
        logging.error(traceback.format_exc())
        return jsonify({'error': 'Failed to fetch weather summary'}), 500

@app.route('/daily_summary', methods=['GET'])
def daily_summary():
    try:
        summary = calculate_daily_aggregates()  # Or fetch data
        return jsonify(summary), 200
    except Exception as e:
        logging.error(f"Error in daily_summary endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/check_alerts', methods=['GET'])
def check_alerts():
    try:
        alerts = Alert.query.all()
        return jsonify({'alerts': [alert.serialize() for alert in alerts]}), 200
    except Exception as e:
        logging.error(f"Error checking alerts: {e}")
        return jsonify({'error': 'Failed to fetch alerts'}), 500

@app.route('/weather_trends', methods=['GET'])
def weather_trends():
    try:
        trends = get_weather_trends()
        return jsonify(trends), 200
    except Exception as e:
        logging.error(f"Error fetching weather trends: {e}")
        return jsonify({'error': 'Failed to fetch weather trends'}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content

if __name__ == "__main__":
    app.run(debug=True)
