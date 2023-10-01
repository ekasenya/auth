FROM python:3.7-slim

EXPOSE 8080

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app /code/app

CMD ["python", "/code/app/main.py"]
