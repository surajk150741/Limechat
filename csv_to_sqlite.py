import sqlite3
import pandas as pd
import os

# Directory containing your CSV files
csv_directory = "C://Users//suraj//OneDrive//Desktop//Personal//bhole\limechat//files"

# SQLite database name
db_name = "output.db"

# Create or connect to the SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Get a list of CSV files in the directory
csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]

for csv_file in csv_files:
    # Read CSV file into a Pandas DataFrame
    df = pd.read_csv(os.path.join(csv_directory, csv_file))

    # Extract table name from CSV filename (remove '.csv' extension)
    table_name = os.path.splitext(csv_file)[0]

    # Create table in SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit changes and close connection
conn.commit()
conn.close()

print("CSV files converted and saved to SQLite database:", db_name)
