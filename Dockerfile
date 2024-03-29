FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir --upgrade poetry

COPY . /app

RUN poetry config virtualenvs.in-project true

RUN poetry install

EXPOSE 8080

CMD ["poetry", "run", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
