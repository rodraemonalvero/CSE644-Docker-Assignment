FROM python:3.12-slim

LABEL maintainer="Rod Raemon Alvero"
LABEL course="CSE644 Advanced Cloud Computing"
LABEL description="Python Flask web server running on port 8888"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8888

CMD ["gunicorn", "--bind", "0.0.0.0:8888", "app:app"]