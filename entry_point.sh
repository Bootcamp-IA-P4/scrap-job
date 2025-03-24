#!/bin/bash

# Start PostgreSQL in the background
echo "Starting PostgreSQL..."
service postgresql start

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
while ! pg_isready -q -h localhost -p 5432 -U postgres; do
  sleep 1
done
echo "PostgreSQL started successfully."

# Set up the PostgreSQL user and database
echo "Setting up PostgreSQL user and database..."
su - postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD '$DB_PASSWORD';\""
su - postgres -c "psql -c \"CREATE DATABASE Companies;\""
echo "PostgreSQL user and database setup successfully."

# Start Xvfb (virtual display)
echo "Starting virtual display..."
Xvfb :99 -ac -screen 0 1280x1024x24 &
export DISPLAY=:99

# Set Python path
export PYTHONPATH=/app

# Run Python scripts
echo "Running Python scripts..."
cd /app

# Run database creation script
echo "Running database creation script"
poetry run python3 /app/db/creation.py

# Run scraping script with proper display
echo "Running scrape script"
poetry run python3 /app/scrap_job/scrap.py

# Moving file to expected location
mkdir -p /app/scrap_job/
cp companies.csv /app/scrap_job/companies.csv

# Run database loading script 
echo "Running database loading script"
poetry run python3 /app/db/load_companies.py

# Start the FastAPI application
echo "Starting FastAPI application"
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000

# Keep the container running
tail -f /dev/null