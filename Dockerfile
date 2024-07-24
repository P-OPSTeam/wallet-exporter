FROM python:3.9-slim AS build-env

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

WORKDIR /app
EXPOSE 9877
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages
ENTRYPOINT ["python3", "exporter.py"]