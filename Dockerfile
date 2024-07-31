FROM python:3.11-alpine3.20

WORKDIR /app 

COPY requirements.txt /app/requirements.txt 
RUN pip install -r /app/requirements.txt

COPY . /app/ 

CMD ["python", "entrypoint.py"]
