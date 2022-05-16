
FROM tiangolo/uvicorn-gunicorn:python3.8

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt

COPY . /fastapi

EXPOSE 8000:8000

CMD ["python", "main.py"]