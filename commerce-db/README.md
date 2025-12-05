# Commerce Database Project

This project is designed to manage product data for a commerce website. It includes the necessary files and configurations to set up and run a database that stores product information.

## Project Structure

```
commerce-db
├── sql
│   ├── schema.sql
│   └── seed_products.sql
├── migrations
│   └── V1__create_products_table.sql
├── docker-compose.yml
├── init-db.sh
├── .env.sample
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Environment Variables**
   Copy the `.env.sample` file to `.env` and fill in the required database connection details.

3. **Docker Setup**
   Ensure you have Docker installed. Navigate to the project directory and run:
   ```
   docker-compose up -d
   ```

4. **Initialize the Database**
   Run the initialization script to set up the database schema and seed it with initial data:
   ```
   ./init-db.sh
   ```

## Usage Guidelines

- The `sql/schema.sql` file contains the SQL statements to create the database schema, including the products table.
- The `sql/seed_products.sql` file includes SQL insert statements to populate the products table with example entries.
- The `migrations` directory contains version-controlled migration scripts for managing database changes.
- Use the `docker-compose.yml` file to manage the database service and its configurations.

## Contributing

Feel free to submit issues or pull requests to improve the project. Please ensure that your contributions adhere to the project's coding standards and guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.