# Użycie obrazu Ubuntu 20.04
FROM ubuntu:20.04

# Avoid prompts from apt
ARG DEBIAN_FRONTEND=noninteractive

# Install Python3, pip, i Java
RUN apt-get -y update && apt-get install -y \
    python3-dev \
    python3-pip \
    apt-utils \
    build-essential \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer;
    
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME


# Set JAVA_HOME environment variable
#ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
#ENV PATH=$JAVA_HOME/bin:$PATH

# Upgrade pip to its latest version
RUN pip3 install --upgrade pip

# Aktualizacja setuptools
RUN pip3 install --upgrade setuptools

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["kedro", "run"]