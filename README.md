# Air pollution Inteligent system - Ptuj

For installing dependencies run: `poetry install`
<br>
For Python saving PIP dependencies run: `poetry run pip freeze > requirements.txt`
<br>
For Docker image creation run: `docker build -t iis_air_pollution_api .`
<br>
<br>
DagsHub repository for data: https://dagshub.com/KiwiBrezo/air-pollution-inteligent-system
<br>
<br>
Report for auto data pipeline are deployed here:
<br>
Data Validation: https://air-pollution-is-data-validation.netlify.app
<br>
Data Report: https://air-pollution-is-data-report.netlify.app
<br>
Data Stability: https://air-pollution-is-data-stability.netlify.app

Data used to train the model:
<br>
(Air Pollution) Getting data from (hourly): https://arsoxmlwrapper.app.grega.xyz/api/air/archive

(Weather) Historical data from (hourly): https://open-meteo.com/en/docs/historical-weather-api#latitude=46.42&longitude=15.87&start_date=2023-01-31&end_date=2023-03-01&&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,surface_pressure,cloudcover,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin