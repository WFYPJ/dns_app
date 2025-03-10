FROM python:3.9

WORKDIR /app

COPY FS_server.py .

RUN pip install flask

EXPOSE 9090

CMD ["python", "FS_server.py"]