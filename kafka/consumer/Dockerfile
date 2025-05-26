FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1

USER root
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc procps stress && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /consumer

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./consumer.py .

CMD ["python", "consumer.py"]