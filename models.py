from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime

db = SQLAlchemy()

class WeatherSummary(db.Model):
    __tablename__ = 'weather_summary'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    humidity = db.Column(db.Float, nullable=False)  # New field for humidity
    wind_speed = db.Column(db.Float, nullable=False)  # New field for wind speed
    
    def __repr__(self):
        return f'<WeatherSummary {self.city} on {self.date}>'


class WeatherTrends(db.Model):
    __tablename__ = 'weather_trends'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    trend_date = db.Column(db.Date, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<WeatherTrends {self.city} on {self.trend_date}>'

class DailySummary(db.Model):
    __tablename__ = 'daily_summary'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<DailySummary {self.city} - {self.date}>'
    
class AlertThreshold(db.Model):
    __tablename__ = 'alert_thresholds'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    max_temp = db.Column(db.Float, nullable=False)  # Max temperature threshold
    min_temp = db.Column(db.Float, nullable=True)   # Optional min temperature threshold
    condition = db.Column(db.String(100), nullable=True)  # Optional condition threshold

    def __repr__(self):
        return f'<AlertThreshold {self.city}: max_temp={self.max_temp}>'
    
class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Automatically adds a timestamp

    def serialize(self):
        return {
            'city': self.city,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }

    def __repr__(self):
        return f'<Alert {self.city}: {self.message}>'