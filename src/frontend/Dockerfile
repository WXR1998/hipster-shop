FROM golang:1.14-alpine as builder

ENV PROJECT github.com/lightstep/hipster-shop/src/frontend
WORKDIR /go/src/$PROJECT

# restore dependencies
COPY . .
RUN go install .

FROM docker.peidan.me/wxr20/hipster-shop/chaosblade as chaosblade
RUN env | grep -E "JAVA|LD_LIB|TOMCAT_SHA512|CATALINA|TOMCAT_MAJOR|PATH|LANG|SANDBOX|TOMCAT_VERSION|TOMCAT_NATIVE|CHAOS_HOME" > /root/env.tmp

FROM alpine as release
RUN apk add --no-cache ca-certificates \
    busybox-extras net-tools bind-tools
WORKDIR /frontend
COPY --from=builder /go/bin/frontend /frontend/server
COPY ./templates ./templates
COPY ./static ./static

COPY --from=chaosblade /usr/local/tomcat /usr/local/tomcat
COPY --from=chaosblade /usr/local/chaosblade /usr/local/chaosblade
COPY --from=chaosblade /usr/lib/jvm /usr/lib/jvm
COPY --from=chaosblade /root/env.tmp /root/env.tmp
COPY services.sh .
EXPOSE 8080
RUN env
RUN source /root/env.tmp
RUN env
# ENTRYPOINT ["/frontend/server"]
ENTRYPOINT ["sh", "services.sh"]
