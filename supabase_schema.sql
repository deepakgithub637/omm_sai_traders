-- OMM SAI TRADERS - Supabase Database Schema
-- Run this in your Supabase SQL editor

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    description TEXT,
    image_url TEXT,
    rating DECIMAL(3,1) DEFAULT 4.0,
    brand TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_id TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    customer_email TEXT,
    customer_phone TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method TEXT DEFAULT 'COD',
    notes TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Order Items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Contact messages
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Allow public read for products
CREATE POLICY "Public can read products" ON products FOR SELECT USING (true);

-- Allow public insert for orders and contacts
CREATE POLICY "Anyone can create orders" ON orders FOR INSERT WITH CHECK (true);
CREATE POLICY "Anyone can create contacts" ON contacts FOR INSERT WITH CHECK (true);
CREATE POLICY "Anyone can create order_items" ON order_items FOR INSERT WITH CHECK (true);

-- Sample product data
INSERT INTO products (name, category, price, stock, description, image_url, rating, brand) VALUES
('DAP Fertilizer 50kg', 'fertilizer', 1350.00, 100, 'Di-Ammonium Phosphate - Best for Kharif crops', 'https://placehold.co/400x400/1a472a/white?text=DAP+50kg', 4.8, 'IFFCO'),
('Urea 45kg Bag', 'fertilizer', 266.00, 200, 'Government subsidized urea. Essential nitrogen source for all crops.', 'https://placehold.co/400x400/2d5a27/white?text=UREA+45kg', 4.9, 'NFL'),
('NPK 10-26-26 Fertilizer', 'fertilizer', 1450.00, 80, 'Balanced NPK fertilizer for paddy and vegetables.', 'https://placehold.co/400x400/1b5e20/white?text=NPK', 4.7, 'Coromandel'),
('Chlorpyrifos 20% EC 1L', 'pesticide', 320.00, 150, 'Broad-spectrum insecticide for rice pests.', 'https://placehold.co/400x400/1a237e/white?text=Chlorpyrifos', 4.5, 'Dhanuka'),
('Imidacloprid 17.8% SL', 'pesticide', 480.00, 90, 'Systemic insecticide for sucking pests.', 'https://placehold.co/400x400/283593/white?text=Imidacloprid', 4.6, 'Bayer'),
('Mancozeb 75% WP 500g', 'fungicide', 260.00, 120, 'Protectant fungicide for blast, brown spot.', 'https://placehold.co/400x400/4a148c/white?text=Mancozeb', 4.4, 'Indofil'),
('Glyphosate 41% SL 1L', 'herbicide', 390.00, 110, 'Non-selective systemic herbicide.', 'https://placehold.co/400x400/e65100/white?text=Glyphosate', 4.3, 'Monsanto'),
('Hybrid Paddy Seeds 5kg', 'seeds', 750.00, 60, 'High-yielding hybrid paddy seeds for Odisha.', 'https://placehold.co/400x400/f57f17/white?text=Paddy+Seeds', 4.7, 'Pioneer'),
('Knapsack Sprayer 16L', 'equipment', 1250.00, 30, 'Manual knapsack sprayer with adjustable nozzle.', 'https://placehold.co/400x400/37474f/white?text=Sprayer+16L', 4.8, 'Neptune'),
('Battery Sprayer 12L', 'equipment', 3200.00, 15, 'Rechargeable battery operated sprayer.', 'https://placehold.co/400x400/263238/white?text=Battery+Sprayer', 4.7, 'E-agro');
