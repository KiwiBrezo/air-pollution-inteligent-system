from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from src.models.predict_model import predict_air_pollution
from src.util.cache_air_pollution import get_meteoroloske_data, init_cache

app = FastAPI()

init_cache()


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/air")
async def air_polution_home():
    return {"message": "This is an Air Pollution prediction API"}


@app.get("/air/now/ptuj")
async def get_meteoroloske():
    return get_meteoroloske_data()


@app.post("/air/prediction")
async def air_pollution_prediction(data: List[WeatherData]):
    pred = np.asarray(np.array(predict_air_pollution(data)), dtype='int')

    return {"prediction": pred.tolist()}
