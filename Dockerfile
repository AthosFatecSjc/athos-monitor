FROM python:3.12-slim

WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x /code/wait-for-db.sh
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
CMD ["sh", "wait-for-db.sh"]
