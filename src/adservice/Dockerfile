FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
FROM docker.peidan.me/wxr20/hipster-shop/adservice:base as builder

WORKDIR /app

COPY . .
RUN chmod +x gradlew
RUN ./gradlew installDist

FROM openjdk:8-slim

# Download Stackdriver Profiler Java agent
RUN apt-get -y update && apt-get install -qqy \
    wget \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/cprof && \
    wget -q -O- https://storage.googleapis.com/cloud-profiler/java/latest/profiler_java_agent.tar.gz \
    | tar xzv -C /opt/cprof && \
    rm -rf profiler_java_agent.tar.gz

COPY --from=docker.peidan.me/wxr20/hipster-shop/grpc_health_probe /bin/grpc_health_probe /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe

WORKDIR /app
COPY --from=builder /app .
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY services.sh .

EXPOSE 9555
ENTRYPOINT ["/app/build/install/hipstershop/bin/AdService"]
