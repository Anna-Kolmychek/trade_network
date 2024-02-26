FROM python:3

WORKDIR /trade_network

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
