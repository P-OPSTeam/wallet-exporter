FROM python:3.9-slim AS build-env
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /app
EXPOSE 9877
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages
ENTRYPOINT ["python3", "exporter.py"]