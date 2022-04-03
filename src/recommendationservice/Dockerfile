FROM docker.peidan.me/wxr20/hipster-shop/recommendationservice:base as base
WORKDIR /recommendationservice
COPY . .
ENV PORT "8080"
EXPOSE 8080
ENTRYPOINT [ "bash", "services.sh" ]
