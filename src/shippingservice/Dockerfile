FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
FROM docker.peidan.me/wxr20/hipster-shop/shippingservice:base as builder

WORKDIR /go/src/$PROJECT
COPY . .
RUN go install .

FROM docker.peidan.me/wxr20/hipster-shop/alpine as release
RUN apk add --no-cache ca-certificates bash
COPY --from=docker.peidan.me/wxr20/hipster-shop/grpc_health_probe /bin/grpc_health_probe /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY --from=builder /go/bin/shippingservice /shippingservice
COPY services.sh .

ENV APP_PORT=50051
EXPOSE 50051
ENTRYPOINT ["bash", "services.sh"]
