#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Database connection details
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-commerce}
DB_USER=${DB_USER:-user}
DB_PASSWORD=${DB_PASSWORD:-password}

# Function to execute SQL files
execute_sql() {
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $1
}

# Create the database if it doesn't exist
echo "Creating database if it doesn't exist..."
createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME || echo "Database already exists."

# Execute schema and seed files
echo "Setting up the database schema..."
execute_sql sql/schema.sql

echo "Seeding the database with initial data..."
execute_sql sql/seed_products.sql

echo "Database initialization complete."