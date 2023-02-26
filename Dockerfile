FROM python:3.9
#FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

RUN mkdir -p ./code/data/processed
RUN mkdir -p ./code/data/raw
RUN mkdir -p ./code/models
RUN mkdir -p ./code/reports/figures

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]