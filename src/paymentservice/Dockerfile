FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
FROM docker.peidan.me/wxr20/hipster-shop/paymentservice:base 
WORKDIR /usr/src/app
COPY . .
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY services.sh .
EXPOSE 50051
ENTRYPOINT ["sh", "services.sh"]