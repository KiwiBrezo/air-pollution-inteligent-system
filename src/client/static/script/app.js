$(document).ready(() => {
    getBasicData();
})

function getBasicData() {
    $.ajax({
        url : "https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,precipitation_probability,surface_pressure,cloudcover,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin",
        success : function (data) {
            console.log(data);
            showBasicData(data);
            showGraph(data);
        }
    })
}

function showBasicData(data) {
    $("#basicTemperature").text(data.hourly.temperature_2m[0] + data.hourly_units.temperature_2m)
    $("#basicHumidity").text(data.hourly.relativehumidity_2m[0] + data.hourly_units.relativehumidity_2m)
    $("#basicPrecipitationProbability").text(data.hourly.precipitation_probability[0] + data.hourly_units.precipitation_probability)
    $("#basicWindSpeed").text(data.hourly.windspeed_10m[0] + data.hourly_units.windspeed_10m)
}

function showGraph(data) {
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
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