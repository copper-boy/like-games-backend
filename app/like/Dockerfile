FROM ubuntu:latest

WORKDIR /app/build

RUN apt update && \
    apt install -y \
    git \
    gcc g++ \
    build-essential cmake make \
    libboost-all-dev \
    libjsoncpp-dev uuid-dev zlib1g-dev

CMD echo "[+] Compiling drogon app..." && \
    cmake .. && make && \
    ./like
