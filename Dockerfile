FROM ubuntu

# Install Python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

#Install Java
RUN apt-get update && apt-get install -y default-jdk

RUN apt-get update && apt-get install -y \
    curl \
    xz-utils

RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev

# Install Infer
RUN VERSION=1.1.0; \
    curl -sSL "https://github.com/facebook/infer/releases/download/v${VERSION}/infer-linux64-v${VERSION}.tar.xz" \
    | tar -C /opt -xJ && \
    ln -s "/opt/infer-linux64-v${VERSION}/bin/infer" /usr/local/bin/infer

# Install Ollama
RUN curl -fsSL -o install.sh -L https://ollama.com/install.sh && chmod +x install.sh && ./install.sh

RUN ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime && echo "Europe/London" > /etc/timezone

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y tzdata

WORKDIR /app

COPY . .

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

