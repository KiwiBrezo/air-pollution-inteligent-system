For Python PIP dependencies run: `poetry run pip freeze > requirements.txt`
<br>
For Docker image creation run: `docker build -t iis_air_pollution_api .`
<br>
(Air Pollution) Getting data from: `https://arsoxmlwrapper.app.grega.xyz/api/air/archive`
<br>
(Weather) Historical data from: `https://open-meteo.com/en/docs/historical-weather-api#latitude=46.42&longitude=15.87&start_date=2023-01-31&end_date=2023-03-01&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,shortwave_radiation_sum,precipitation_sum,rain_sum,precipitation_hours,windspeed_10m_max,winddirection_10m_dominant&timezone=Europe%2FBerlin`
<br>
(Weather) Forecast data from: `https://open-meteo.com/en/docs#latitude=46.42&longitude=15.87&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,rain_sum,precipitation_hours,windspeed_10m_max,winddirection_10m_dominant,shortwave_radiation_sum&timezone=Europe%2FBerlin`