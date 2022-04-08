FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
FROM docker.peidan.me/wxr20/hipster-shop/checkoutservice:base as builder
WORKDIR /go/src/$PROJECT

COPY . .
RUN go build -gcflags='-N -l' -o /checkoutservice .

FROM docker.peidan.me/wxr20/hipster-shop/alpine as release
RUN apk add --no-cache ca-certificates bash openssh sshpass
COPY --from=docker.peidan.me/wxr20/hipster-shop/grpc_health_probe /bin/grpc_health_probe /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe
COPY --from=builder /checkoutservice /checkoutservice
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY services.sh .
EXPOSE 5050

ENTRYPOINT ["bash", "services.sh"]
