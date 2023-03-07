from fastapi import FastAPI
from pydantic import BaseModel
from src.models.predict_model import predict_air_pollution

app = FastAPI()


class WeatherData(BaseModel):
    datum_do: str
    temperature: float
    relativehumidity: float
    dewpoint: float
    surface_pressure: float
    cloudcover: float
    windspeed: float
    winddirection: float
    pm25: int


@app.get("/air")
async def air_polution_home():
    return {"message": "This is an Air Pollution prediction API"}


@app.post("/air/prediction")
async def air_pollution_prediction(data: WeatherData):
    pred = int(predict_air_pollution(data))
    return {"prediction": pred}
