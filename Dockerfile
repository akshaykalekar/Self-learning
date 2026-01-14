FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py test.py .

# Document ports (for humans + tools)
EXPOSE 8080
EXPOSE 9090

# Default: run tests
CMD ["pytest", "-v"]
