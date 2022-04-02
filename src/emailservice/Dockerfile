FROM docker.peidan.me/wxr20/hipster-shop/emailservice:base as base
WORKDIR /email_server
# Add the application
COPY . .

EXPOSE 8080
ENTRYPOINT ["sh", "services.sh"]
