FROM python:3-alpine

# python print tty
ENV PYTHONUNBUFFERED=0

COPY target-app.py /target-app.py

RUN chmod +x /target-app.py
RUN pip3 install prometheus_client

ENTRYPOINT ["python3","-u","target-app.py"]