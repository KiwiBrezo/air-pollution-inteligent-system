FROM python:3.9

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade poetry
RUN poetry install --no-root --without dev

COPY ./src /code/src

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.serve.air_pollution_controller:app", "--host", "0.0.0.0", "--port", "8000"]