import psycopg2
import pandas as pd
import urllib.parse
import os
import sys
import getpass

# Read URI parameters from the environment
dbhost = "customchatbotdbserver.postgres.database.azure.com"
dbname = "testdb"
sslmode = "prefer"

# Prompt the user for the password securely
dbuser = input('Enter your PostgreSQL DB username: ')
password = getpass.getpass(prompt='Enter your PostgreSQL password: ')

# Connection string
conn_string = f"host={dbhost} dbname={dbname} user={dbuser} password={password} sslmode={sslmode}"

# Connect to the PostgreSQL server
conn = psycopg2.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_directory}")

# Construct the file directory
xslx_file_dir = os.path.join(script_directory, 'sample_data')
print(f"CSV file directory: {xslx_file_dir}")

# Path to the file
xlsx_file_path = os.path.join(xslx_file_dir, 'products_data.xlsx')
print(f"Excel file path: {xlsx_file_path}")

# Check if the Excel file exists
if not os.path.exists(xlsx_file_path):
    print(f"Excel file does not exist: {xlsx_file_path}")
    sys.exit(1)

# Read the Excel file into a DataFrame, specifying the sheet name
df = pd.read_excel(xlsx_file_path, sheet_name='products')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Insert data into the products table
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO products (id, product_name, price, category, brand, product_description) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            row['id'],
            row['product_name'],
            row['price'],
            row['category'],
            row['brand'],
            row['product_description']
        )
    )

print("Inserted rows from sample data file into the products table")

# Commit the transaction and close connections
conn.commit()
cursor.close()
conn.close()