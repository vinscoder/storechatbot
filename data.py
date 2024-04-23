import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('goods.db')
cursor = conn.cursor()

# Create a table for goods
cursor.execute('''CREATE TABLE goods (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL)''')

goods_data = [
('Apple Watch', 'A smartwatch by Apple with a sleek design and advanced features.'),
('Samsung TV', 'A high-quality 4K TV by Samsung with a wide viewing angle and smart capabilities.'),
('Bose Headphones', 'High-fidelity wireless headphones by Bose with noise-canceling technology.'),
('Dyson Vacuum', 'A powerful cordless vacuum cleaner by Dyson with advanced cyclonic technology.')
]

cursor.executemany('INSERT INTO goods (name, description) VALUES (?, ?)', goods_data)

# Commit the transaction and close the connection
conn.commit()
conn.close()