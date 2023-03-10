FROM python:3.9
#FROM python:3.9-alpine     #not working ok

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

RUN mkdir -p ./data/processed
RUN mkdir -p ./data/raw/air
RUN mkdir -p ./data/raw/weather
RUN mkdir -p ./models
RUN mkdir -p ./reports/figures

RUN python ./src/data/fetch_data.py
RUN python ./src/models/train_model.py

EXPOSE 8000

CMD ["uvicorn", "src.serve.air_pollution_controller:app", "--host", "0.0.0.0", "--port", "8000"]