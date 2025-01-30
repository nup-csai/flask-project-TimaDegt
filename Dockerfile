FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app/server.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["flask", "--app", "app/server.py", "run", "-h", "0.0.0.0", "-p", "8080"]