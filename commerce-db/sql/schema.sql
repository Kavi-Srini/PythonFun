CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    size VARCHAR(50),
    description TEXT,
    price_cents INTEGER NOT NULL,
    stock INT NOT NULL,
    featured BOOLEAN DEFAULT FALSE,
    sku VARCHAR(64) NOT NULL
);

