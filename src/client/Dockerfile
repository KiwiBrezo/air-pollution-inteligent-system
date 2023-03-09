FROM golang:1.19-alpine

WORKDIR /app

COPY go.mod ./
RUN go mod download

COPY . ./

RUN mkdir files

RUN go build -o /air_pollution_frontend

EXPOSE 80

CMD [ "/air_pollution_frontend" ]
