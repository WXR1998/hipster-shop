FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
FROM docker.peidan.me/wxr20/hipster-shop/currencyservice:base as builder
FROM docker.peidan.me/wxr20/hipster-shop/node:14-alpine as base

RUN apk add --no-cache bash openssh sshpass
COPY --from=docker.peidan.me/wxr20/hipster-shop/grpc_health_probe /bin/grpc_health_probe /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY services.sh .

COPY . .

EXPOSE 7000

ENTRYPOINT ["bash", "services.sh"]
