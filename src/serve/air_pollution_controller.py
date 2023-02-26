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


@app.post("/air/prediction")
async def air_pollution_prediction(data: AirData):
    pred = predict_air_pollution(data)
    return {"prediction": pred}
