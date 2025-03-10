FROM python:3.9

WORKDIR /app

COPY US_server.py .

RUN pip install flask requests

EXPOSE 8080

CMD ["python", "US_server.py"]