// static/js/dashboard.js

// Sample data for testing
let currentData = {
    AMBIENT_TEMPERATURE: 25.0,
    GROUND_TEMPERATURE: 20.0,
    WIND_DIRECTION: 180.0,
    WIND_SPEED: 15.0,
    WIND_GUST_SPEED: 20.0,
    RAINFALL: 5.0,
    AIR_PRESSURE: 1015.0,
    HUMIDITY: 60.0,
    DEWPOINT: 18.0,
    CREATED: '2024-02-17 12:00:00'
};

let historicalRainfallData = [3.0, 2.0, 1.5, 4.0, 2.5, 3.0, 1.0];  // Replace with your historical rainfall data
let historicalPressureData = [1010.0, 1012.0, 1014.0, 1016.0, 1018.0, 1015.0, 1013.0];  // Replace with your historical pressure data

// Initial unit settings
let temperatureUnit = 'C';
let speedUnit = 'km/h';
let pressureUnit = 'hPa';
let rainfallUnit = 'mm';

document.addEventListener("DOMContentLoaded", function () {
    // Code to run when the DOM is fully loaded

    // Fetch and update data initially
    //fetchCurrentDataAndUpdateDashboard();

    // Set interval to update date and time every minute
    setInterval(updateDateTime, 60000);

    // Set interval to fetch current weather data and update data every 20 seconds
    setInterval(updateCurrentDashboard, 20 * 1000);

    // Set interval to fetch historical weather data and update the graphs every 5 minutes
    setInterval(fetchHistoricalDataAndUpdateGraphs, 5 * 60 * 1000);

    // Navigation bar button click handler
    const navBarButton = document.getElementById("nav-bar");
    navBarButton.addEventListener("click", toggleNavBar);

    // Unit settings button click handlers for each unit
    const temperatureSettingsButton = document.getElementById("temperature-settings");
    const rainfallSettingsButton = document.getElementById("rainfall-settings");
    const speedSettingsButton = document.getElementById("speed-settings");
    const pressureSettingsButton = document.getElementById("pressure-settings");

    temperatureSettingsButton.addEventListener("click", toggleTemperatureUnit);
    rainfallSettingsButton.addEventListener("click", toggleRainfallUnit);
    speedSettingsButton.addEventListener("click", toggleSpeedUnit);
    pressureSettingsButton.addEventListener("click", togglePressureUnit);

    // Display initial data
    updateCurrentDashboard(currentData);

    // Add more code for other interactions or functionality
});

function toggleTemperatureUnit() {
    // Toggle temperature units between C, F, and K
    if (temperatureUnit === 'C') {
        temperatureUnit = 'F';
    } else if (temperatureUnit === 'F') {
        temperatureUnit = 'K';
    } else {
        temperatureUnit = 'C';
    }
    updateCurrentDashboard(currentData);
}

function toggleRainfallUnit() {
    // Toggle rainfall units between mm and inches
    rainfallUnit = (rainfallUnit === 'mm') ? 'inches' : 'mm';
    updateCurrentDashboard(currentData);
}

function toggleSpeedUnit() {
    // Toggle speed units between km/h and mph
    speedUnit = (speedUnit === 'km/h') ? 'mph' : 'km/h';
    updateCurrentDashboard(currentData);
}

function togglePressureUnit() {
    // Toggle pressure units between hPa and inHg
    pressureUnit = (pressureUnit === 'hPa') ? 'inHg' : 'hPa';
    updateCurrentDashboard(currentData);
}

function toggleNavBar() {
    const navBar = document.getElementById("nav-bar");
    navBar.style.display = (navBar.style.display === "none" || navBar.style.display === "") ? "block" : "none";
}

function updateDateTime() {
    console.log('Updating date and time...');
    // Update date and time
    const dateTimeElement = document.getElementById("date-time");
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString();
    const formattedTime = currentDate.toLocaleTimeString();
    dateTimeElement.textContent = `${formattedDate} ${formattedTime}`;
}

function fetchCurrentDataAndUpdateDashboard() {
    // Log before making the request
    console.log('Fetching data from /api/current_data');
    
    // Fetch current weather data from the server (assuming you have an endpoint /api/current_data)
    fetch("/api/current_data")
        .then(response => response.json())
        .then(currentData => {
            // Log after receiving the response
            console.log('Received data:', currentData);
            
            // Update the dashboard with the fetched current data
            updateCurrentDashboard(currentData);
        })
        .catch(error => {
            console.error("Error fetching current data:", error);
        });
}

function fetchHistoricalDataAndUpdateGraphs() {
    // Fetch historical data from the server (assuming you have an endpoint /api/historical_data)
    fetch("/api/historical_data")
        .then(response => response.json())
        .then(historicalData => {
            // Update the arrays with the fetched historical data
            historicalRainfallData = historicalData.rainfallData;
            historicalPressureData = historicalData.pressureData;
            // Update the graphs with the fetched historical data
            updateGraphs(historicalData);
        })
        .catch(error => {
            console.error("Error fetching historical data:", error);
        });
}

function updateCurrentDashboard(data) {
    // Example: Update the dashboard elements with the fetched data and current unit settings
    document.getElementById("air-temperature").textContent = formatTemperature(data.AMBIENT_TEMPERATURE);
    document.getElementById("humidity").textContent = data.HUMIDITY + ' %';
    document.getElementById("wind-speed").textContent = data.WIND_SPEED + ' ' + speedUnit;
    document.getElementById("wind-gust").textContent = data.WIND_GUST_SPEED + ' ' + speedUnit;
    const currentRainfall = formatRainfall(data.RAINFALL);
    document.getElementById("current-rainfall").textContent = formatRainfall(data.RAINFALL) + ' ' + rainfallUnit;
    document.getElementById("ground-temperature").textContent = formatTemperature(data.GROUND_TEMPERATURE); 
    const currentPressure =  formatPressure(data.AIR_PRESSURE);  
    document.getElementById("current-pressure").textContent = data.AIR_PRESSURE + ' ' + pressureUnit;
    document.getElementById("dewpoint").textContent = formatTemperature(data.DEWPOINT);
    document.getElementById("date-time").textContent = data.CREATED;

    // Update the bar graph for rainfall
    updateRainGraph(historicalRainfallData, currentRainfall);

    // Update the line graph for barometric pressure
    updatePressureGraph(historicalPressureData, currentPressure);
    
    // Update wind direction and arrow
    const windDegreesElement = document.getElementById("wind-direction-degrees");
    const windCardinalElement = document.getElementById("wind-direction-cardinal");
    const arrowElement = document.getElementById("arrow");

    const windDegrees = data.WIND_DIRECTION;
    const cardinalDirection = degrees_to_cardinal(windDegrees);

    windDegreesElement.textContent = `${windDegrees}°`;
    windCardinalElement.textContent = cardinalDirection;

    // Update the arrow rotation based on wind direction
    arrowElement.style.transform = `rotate(${windDegrees}deg)`;
    console.log(data.WIND_DIRECTION);
    

    // Update other elements as needed
}

// Function to convert degrees to cardinal direction
function degrees_to_cardinal(angle) {
    const directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
    const ix = Math.round((angle + 11.25) / 22.5);
    return directions[ix % 16];
}

function formatTemperature(value) {
    // Convert temperature based on the current temperatureUnit
    if (temperatureUnit === 'F') {
        return (value * 9/5) + 32 + ' °F';
    } else if (temperatureUnit === 'K') {
        return value + 273.15 + ' °K';
    } else {
        return value + ' °C';
    }
}

function formatRainfall(value) {
    // Convert rainfall based on the current rainfallUnit
    if (rainfallUnit === 'inches') {
        return value * 0.0393701 + ' inches';
    } else {
        return value + ' mm';
    }
}

function formatPressure(value) {
    // Conver pressure based on current pressureUnit
    if (pressureUnit === 'inHg') {
        return value * 0.02953 + ' inHg';
    } else {
        return value + ' hPa';
    }
}

function updateRainGraph(historicalRainfallData, currentRainfall) {
    // Update the bar graph for rainfall using Chart.js
    const ctx = document.getElementById("rainGraph").getContext("2d");

    const rainChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: historicalRainfallData.map((_, index) => index + 1),
            datasets: [{
                label: 'Rainfall (mm)',
                data: historicalRainfallData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    document.getElementById("current-rainfall").textContent = currentRainfall;
}

function updatePressureGraph(historicalPressureData, currentPressure) {
    // Update the line graph for barometric pressure using Chart.js
    const ctx = document.getElementById("pressureGraph").getContext("2d");

    const pressureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalPressureData.map((_, index) => index + 1),
            datasets: [{
                label: 'Barometric Pressure (hPa)',
                data: historicalPressureData,
                borderColor: 'rgba(255, 99, 132, 0.2)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    document.getElementById("current-pressure").textContent = currentPressure;
}

function updateGraphs(historicalData) {
    // Update the graphs with the fetched historical data
    // Use a charting library (e.g., Chart.js) to plot the data on your graphs
    // Example:
    var rainfallChart = new Chart(document.getElementById('rainfallChart'), {
        type: 'bar',
        data: {
            labels: historicalData.rainfallLabels,
            datasets: [{
                label: 'Rainfall (mm)',
                data: historicalData.rainfallData,
                backgroundColor: 'blue',
            }]
        },
        options: {
            // Add any additional chart options as needed
        }
    });

    var pressureChart = new Chart(document.getElementById('pressureChart'), {
        type: 'line',
        data: {
            labels: historicalData.pressureLabels,
            datasets: [{
                label: 'Barometric Pressure (hPa)',
                data: historicalData.pressureData,
                borderColor: 'lightgrey',
                fill: false,
            }]
        },
        options: {
            // Add any additional chart options as needed
        }
    });
}
