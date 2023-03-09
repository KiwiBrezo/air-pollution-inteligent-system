$(document).ready(() => {
    getBasicData();
    getBasicPollutionData()
})

function getBasicData() {
    $.ajax({
        url : "https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,precipitation_probability,surface_pressure,cloudcover,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin",
        success : function (data) {
            showBasicData(data);
        }
    })
}

function showBasicData(data) {
    $("#basicTemperature").text(data.hourly.temperature_2m[0] + data.hourly_units.temperature_2m)
    $("#basicHumidity").text(data.hourly.relativehumidity_2m[0] + data.hourly_units.relativehumidity_2m)
    $("#basicPrecipitationProbability").text(data.hourly.precipitation_probability[0] + data.hourly_units.precipitation_probability)
    $("#basicWindSpeed").text(data.hourly.windspeed_10m[0] + data.hourly_units.windspeed_10m)
}

function getBasicPollutionData() {
    $.ajax({
        url : "http://localhost:8000/air/now/ptuj",
        success : function (data) {
            let meteoroloske_data = data.sort(function(a,b){
                return new Date(a.datum_od) - new Date(b.datum_od);
            });

            let last_measure = meteoroloske_data.slice(-1)[0] || { "pm2.5" : "/", "pm10" : "/" }

            $("#basicPm25").text(last_measure["pm2.5"] + "µg/m³")
            $("#basicPm10").text(last_measure["pm10"] + "µg/m³")

            let pm25Arr = meteoroloske_data.slice(-1 * 24 * 21).map((obj) => typeof obj["pm2.5"] === "number" ? obj["pm2.5"] : 1 )
            let pm25Average = pm25Arr.reduce((a, b) => a + b, 0) / pm25Arr.length

            getForecastData(pm25Average);
        }
    })
}

function getForecastData(pm25_value) {
    $.ajax({
        url : "https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,surface_pressure,cloudcover,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin",
        success : function (data) {
            let preparedData = [];

            for (let i = 0; i < data.hourly.time.length || 0; i++) {
                preparedData.push({
                    datum_do : data.hourly.time[i].replace("T", " "),
                    temperature : data.hourly.temperature_2m[i],
                    relativehumidity : data.hourly.relativehumidity_2m[i],
                    dewpoint : data.hourly.dewpoint_2m[i],
                    surface_pressure : data.hourly.surface_pressure[i],
                    cloudcover : data.hourly.cloudcover[i],
                    windspeed : data.hourly.windspeed_10m[i],
                    winddirection : data.hourly.winddirection_10m[i],
                    pm25 : pm25_value,
                })
            }

            getForecastAirPollution(preparedData);
        }
    })
}

function getForecastAirPollution(preparedData) {
    $.ajax({
        type : "POST",
        url : "http://localhost:8000/air/prediction",
        contentType: 'application/json',
        data : JSON.stringify(preparedData),
        processData: false,
        success : function (data) {
            showGraph(preparedData, data.prediction);
        }
    })
}

function showGraph(weatherData, predictedAirPullutionData) {
    let arrOfDates = weatherData.map((obj) => obj["datum_do"])//.slice(0, 3);
    let arrOfPollution = predictedAirPullutionData//.slice(0, 3)

    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: arrOfDates,
            datasets: [{
                label: 'Value of PM10 particles',
                data: arrOfPollution,
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
}