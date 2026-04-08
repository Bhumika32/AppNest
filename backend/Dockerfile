FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for postgres/psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "passlib[bcrypt]" "python-socketio[client]" "psycopg2-binary"

# Copy source code
COPY . .

# Expose API port
EXPOSE 5000

# Start ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]
