FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
FROM docker.peidan.me/wxr20/hipster-shop/productcatalogservice:base as builder
WORKDIR /go/src/$PROJECT

COPY . .
RUN go build -o /productcatalogservice .

FROM docker.peidan.me/wxr20/hipster-shop/alpine AS release
RUN apk add --no-cache ca-certificates bash
COPY --from=docker.peidan.me/wxr20/hipster-shop/grpc_health_probe /bin/grpc_health_probe /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe
WORKDIR /productcatalogservice
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY --from=builder /productcatalogservice ./server
COPY products.json .
COPY services.sh .
EXPOSE 3550
ENTRYPOINT ["bash", "services.sh"]

