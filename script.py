# This script is made to run and execute python commands at a large scale eg database query

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create the table
cursor.execute('''
    CREATE TABLE myapp_productimage_categories (
        id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL,
        image_url TEXT NOT NULL
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()