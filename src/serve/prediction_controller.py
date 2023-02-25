from fastapi import FastAPI

app = FastAPI()


@app.get("/prediction")
async def air_pollution_prediction():
    return {"message": "Hello World"}