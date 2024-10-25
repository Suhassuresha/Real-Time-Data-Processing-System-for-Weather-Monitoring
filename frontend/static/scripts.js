document.addEventListener('DOMContentLoaded', () => {
    // Example: Updating temperature for different cities
    const cityTemps = {
        city1: 25,
        city2: 28,
        city3: 22,
        delhi: 30,
        mumbai: 29,
        chennai: 31,
        bangalore: 24,
        kolkata: 26,
        hyderabad: 27
    };

    // Function to safely update temperature text
    function updateTemperature(cityId, temp) {
        const tempElement = document.getElementById(cityId);
        if (tempElement) {
            tempElement.textContent = `${temp}°C`;
        } else {
            console.warn(`Element with ID '${cityId}' not found.`);
        }
    }

    // Updating temperatures in the HTML
    updateTemperature('city1-temp', cityTemps.city1);
    updateTemperature('city2-temp', cityTemps.city2);
    updateTemperature('city3-temp', cityTemps.city3);
    updateTemperature('delhi-temp', cityTemps.delhi);
    updateTemperature('mumbai-temp', cityTemps.mumbai);
    updateTemperature('chennai-temp', cityTemps.chennai);
    updateTemperature('bangalore-temp', cityTemps.bangalore);
    updateTemperature('kolkata-temp', cityTemps.kolkata);
    updateTemperature('hyderabad-temp', cityTemps.hyderabad);

    // Function to check and display weather alerts
    function updateAlerts() {
        const alertMessage = document.getElementById('alert-message');
        const alertsExist = false; // Example: set to true if there's an actual alert

        if (alertsExist) {
            alertMessage.textContent = "Severe Thunderstorm Warning!";
            alertMessage.classList.add('alert');
        } else {
            alertMessage.textContent = "No weather alerts currently.";
            alertMessage.classList.remove('alert');
            alertMessage.classList.add('no-alerts');
        }
    }

    // Call the updateAlerts function
    updateAlerts();

    // Weather trend data for the charts
    const weatherData = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature (°C) - Delhi',
            data: [30, 32, 31, 29, 28, 27, 26],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    const weatherDataMumbai = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature (°C) - Mumbai',
            data: [29, 30, 31, 32, 30, 29, 28],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    const weatherDataChennai = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature (°C) - Chennai',
            data: [31, 32, 33, 34, 31, 30, 29],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    const weatherDataBangalore = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature (°C) - Bangalore',
            data: [24, 25, 26, 27, 26, 25, 24],
            borderColor: 'rgba(255, 206, 86, 1)',
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    const weatherDataKolkata = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature (°C) - Kolkata',
            data: [26, 27, 28, 29, 28, 27, 26],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    const weatherDataHyderabad = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Temperature (°C) - Hyderabad',
            data: [27, 28, 29, 30, 29, 28, 27],
            borderColor: 'rgba(153, 102, 255, 1)',
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    // Create charts for each city
    const ctxDelhi = document.getElementById('delhiChart').getContext('2d');
    const delhiChart = new Chart(ctxDelhi, {
        type: 'line',
        data: weatherData,
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });

    const ctxMumbai = document.getElementById('mumbaiChart').getContext('2d');
    const mumbaiChart = new Chart(ctxMumbai, {
        type: 'line',
        data: weatherDataMumbai,
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });

    const ctxChennai = document.getElementById('chennaiChart').getContext('2d');
    const chennaiChart = new Chart(ctxChennai, {
        type: 'line',
        data: weatherDataChennai,
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });

    const ctxBangalore = document.getElementById('bangaloreChart').getContext('2d');
    const bangaloreChart = new Chart(ctxBangalore, {
        type: 'line',
        data: weatherDataBangalore,
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });

    const ctxKolkata = document.getElementById('kolkataChart').getContext('2d');
    const kolkataChart = new Chart(ctxKolkata, {
        type: 'line',
        data: weatherDataKolkata,
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });

    const ctxHyderabad = document.getElementById('hyderabadChart').getContext('2d');
    const hyderabadChart = new Chart(ctxHyderabad, {
        type: 'line',
        data: weatherDataHyderabad,
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });
});
