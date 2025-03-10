FROM python:3.9

WORKDIR /app

COPY AS_server.py .

RUN apt update && apt install -y netcat-openbsd && pip install flask

EXPOSE 53533/udp

CMD ["python", "AS_server.py"]