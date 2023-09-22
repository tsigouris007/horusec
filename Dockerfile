FROM golang:1.17-alpine AS builder

USER root
WORKDIR /

# Download and build
RUN apk update
RUN apk add --no-cache git
RUN git clone https://github.com/ZupIT/horusec.git

WORKDIR /horusec
RUN go mod download
RUN env GOOS=linux go build -ldflags '-s -w' -o /bin/horusec ./cmd/app/main.go

FROM alpine:latest

# Install extra dependencies
RUN apk update
RUN apk add --no-cache git jq grep python3 curl

# Create a user
RUN adduser -D -g '' user

# Copy to the user
COPY --from=builder /bin/horusec /usr/local/bin
COPY --from=builder /horusec/horusec-config.json /data/horusec-config.json
RUN chmod +x /usr/local/bin/horusec
RUN chown user:user /data/horusec-config.json

# Copy the entrypoint
WORKDIR /
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY report.py /report.py
RUN chmod +x /report.py

USER user
WORKDIR /data

ENTRYPOINT [ "/entrypoint.sh" ]
