function fetchWeatherSummary() {
    fetch('/weather_summary')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Weather Summary Data:', data);  // Debugging output
            updateSummary(data);
        })
        .catch(error => showError('summary-content', error));
}

function fetchDailySummary() {
    fetch('/daily_summary')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Daily Summary Data:', data);  // Debugging output
            updateDailySummary(data);
        })
        .catch(error => showError('daily-summary-content', error));
}

function fetchAlerts() {
    fetch('/check_alerts')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Alerts Data:', data);  // Debugging output
            updateAlerts(data.alerts);
        })
        .catch(error => showError('alert-section', error));
}

// function fetchWeatherTrends() {
//     fetch('/weather_trends')
//         .then(response => response.json())
//         .then(trendsData => createWeatherChart('weatherChart', trendsData))
//         .catch(error => console.error('Error fetching weather trends:', error));
// }

function updateSummary(data) {
    const summaryContent = document.getElementById('summary-content');
    summaryContent.innerHTML = ''; // Clear previous content
    data.forEach(city => {
        const citySummary = document.createElement('div');
        citySummary.classList.add('city-summary');
        citySummary.innerHTML = `
            <strong>${city.city}</strong>: 
            Temperature: <span id="${city.city}-temp">${city.temperature}°C</span>
            <div>Condition: ${city.condition}</div>
            <div>Humidity: <span id="${city.city}-humidity">${city.humidity}%</span></div>
            <div>Wind Speed: <span id="${city.city}-wind-speed">${city.wind_speed} m/s</span></div>
        `;
        summaryContent.appendChild(citySummary);
    });
}

function updateDailySummary(data) {
    const summaryContent = document.getElementById('daily-summary-content');
    summaryContent.innerHTML = ''; // Clear previous content

    if (!Array.isArray(data)) {
        console.error('Expected an array for daily summary, but received:', data);
        return;
    }

    data.forEach(entry => {
        const citySummary = document.createElement('div');
        citySummary.classList.add('city-summary');
        citySummary.innerHTML = `
            <strong>${entry.city}</strong>:
            <div>Average Temperature: <span>${entry.average_temperature}°C</span></div>
            <div>Max Temperature: <span>${entry.max_temperature}°C</span></div>
            <div>Min Temperature: <span>${entry.min_temperature}°C</span></div>
            <div>Dominant Condition: <span>${entry.dominant_condition}</span></div>
        `;
        summaryContent.appendChild(citySummary);
    });
}


function updateAlerts(alerts) {
    const alertContent = document.getElementById('alert-message');
    alertContent.innerHTML = ''; // Clear previous alerts

    if (alerts.length > 0) {
        alerts.forEach(alert => {
            const alertDiv = document.createElement('div');
            alertDiv.classList.add('alert');
            alertDiv.innerHTML = `<strong>${alert.city}</strong>: ${alert.message}`;
            alertContent.appendChild(alertDiv);
        });
    } else {
        alertContent.innerHTML = "No weather alerts currently.";
    }
}

function showError(elementId, error) {
    console.error(error);
    document.getElementById(elementId).innerHTML = 'Failed to load data.';
}

function initializePage() {
    fetchWeatherSummary();
    fetchDailySummary();
    fetchAlerts();
    //fetchWeatherTrends();
}

window.onload = initializePage;
