FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the artifacts directory inside the container
RUN mkdir -p /app/artifacts

COPY . .

EXPOSE 3000

CMD ["dagster", "dev", "-f", "dagster_orchestration/repo.py", "-h", "0.0.0.0", "-p", "3000"]