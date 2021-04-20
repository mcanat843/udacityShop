FROM python:3.7-slim
RUN apt-get update -qqy && \
	apt-get -qqy install wget g++ && \
	rm -rf /var/lib/apt/lists/*
# show python logs as they occur
ENV PYTHONUNBUFFERED=0

# download the grpc health probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.3.6 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

# TODO: Place Dockerfile instructions below
WORKDIR /app
COPY . .
EXPOSE 9556
RUN pip install -r requirements.txt

CMD python adservice-v2_server.py