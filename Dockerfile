FROM python:3.9

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Run both Flask and monitor (using a simple script)
COPY run.sh .
RUN chmod +x run.sh

CMD ["./run.sh"]
