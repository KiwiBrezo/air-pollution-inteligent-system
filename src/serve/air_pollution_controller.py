from fastapi import FastAPI
from pydantic import BaseModel
from src.models.predict_model import predict_air_pollution

app = FastAPI()


class AirData(BaseModel):
    datum_do: str
    ge_dolzina: float
    ge_sirina: float
    merilno_mesto: str
    nadm_visina: int
    pm25: int
    sifra: str


@app.get("/air")
async def air_polution_home():
    return {"message": "This is an Air Pollution prediction API"}


@app.post("/air/prediction")
async def air_pollution_prediction(data: AirData):
    pred = int(predict_air_pollution(data))
    return {"prediction": pred}
