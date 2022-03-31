FROM locustio/locust:latest
COPY locustfile.py .
COPY data.py .
COPY period.csv .
ENV HOURLY_SCALE 1.0
RUN pip install pandas numpy
RUN python locustfile.py
ENTRYPOINT locust --headless --host=http://${FRONTEND_ADDR}

