FROM docker.peidan.me/wxr20/hipster-shop/locust:normal
COPY locustfile.py .
COPY data.py .
COPY period.csv .
ENV HOURLY_SCALE 1.0
ENTRYPOINT locust --headless --host=http://${FRONTEND_ADDR}

