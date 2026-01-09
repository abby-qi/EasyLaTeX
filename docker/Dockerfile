FROM node:18-bullseye-slim

LABEL maintainer="EasyLaTeX Team"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    wine64 \
    wine32 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh

ENV PATH="/root/.TinyTeX/bin/x86_64-linux:${PATH}"

COPY package*.json ./
RUN npm install

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

RUN npm run build:linux

CMD ["npm", "start"]