# Weather Monitoring Application

## Overview
The Weather Monitoring Application is a full-stack application that provides real-time weather data and alerts. It allows users to configure thresholds for weather conditions and visualize trends over time.

## Table of Contents
1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Run the Application](#run-the-application)

## Installation
To set up the project, clone the repository and install the necessary dependencies.

```bash
   git clone https://github.com/Suhassuresha/Real-Time-Data-Processing-System-for-Weather-Monitoring.git
   cd weather-monitoring-app
   ```

## Dependencies
- **Python**: Version 3.6 or higher
- **Flask**: Web framework for Python
- **SQLite**: Database for storing weather data
- **Requests**: For making HTTP requests to external APIs
- **Matplotlib**: For generating visualizations of weather data


```bash
pip install -r requirements.txt
```
## Configuration
Ensure your environment variables are set up correctly. The application requires a .env file in the root directory for configuration.

## Usage
To use this application, follow these steps:

Start the database and any required services (if applicable).
Configure your weather monitoring settings as needed.
   - Make sure to have the required database set up (SQLite used in this application).

## Run the Application
Run the application using the following command:
   ```bash
   flask run
   ```

## Design Choices
- **Frameworks Used**: The backend is built using Flask, allowing for a lightweight and flexible structure.
- **Database**: SQLite is used for simplicity and ease of use during development. In production, consider migrating to a more robust database like PostgreSQL.
- **API Integration**: The application uses OpenWeatherMap API to fetch weather data.


## Web Server Methods
The following methods are implemented in the web server:

1. GET /weather_summary
Description: Fetches the current weather summary data.
Response: JSON object containing the current weather details.
2. GET /daily_summary
Description: Retrieves daily weather summaries, including averages, maximum, and minimum temperatures.
Response: JSON object with summary statistics.
3. GET /check_alerts
Description: Fetches the configured user-defined alerts based on weather thresholds.
Response: JSON object containing the list of alerts.
4. GET /weather_trends
Description: Returns weather trends based on historical data.
Response: JSON object containing the weather trends.

## Running with Docker
You can also run the application using Docker. Ensure you have Docker installed and run the following commands:

1. Build the Docker image:
   ```bash
   docker build -t weather-monitoring-app .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 weather-monitoring-app
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
