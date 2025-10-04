import sqlite3

# Connect to the database
conn = sqlite3.connect('database/knowledge_base.db')
cursor = conn.cursor()

print("Database connection successful.")

# Drop the old table to ensure the new schema is applied
cursor.execute("DROP TABLE IF EXISTS tests")

# Create the 'tests' table with the new 'aliases' column
cursor.execute("""
CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    aliases TEXT,
    ref_range_low REAL NOT NULL,
    ref_range_high REAL NOT NULL,
    unit TEXT NOT NULL,
    explanation_low TEXT,
    explanation_high TEXT,
    explanation_normal TEXT
)
""")

print("Table 'tests' created successfully with 'aliases' column.")

# --- New data (with aliases to handle variations) ---
tests_to_add = [
    (
        'Hemoglobin', 'haemoglobin,hgb', 13.2, 16.6, 'g/dL',
        'Low hemoglobin (anemia) means less oxygen is being carried in your blood, which can cause fatigue.',
        'High hemoglobin is often a sign of dehydration or conditions that cause the body to produce too many red blood cells.',
        'Your hemoglobin level, which measures the oxygen-carrying protein in your blood, is normal.'
    ),
    (
        'WBC', 'white blood cell count', 4000, 11000, '/uL',
        'A low white blood cell count can increase your risk of infection.',
        'A high white blood cell count usually indicates that your body is fighting off an infection or inflammation.',
        'Your count of infection-fighting white blood cells is normal.'
    ),
    (
        'Platelets', 'platelet count', 150000, 450000, '/uL',
        'A low platelet count can lead to easy bruising and prolonged bleeding.',
        'A high platelet count can increase the risk of blood clotting.',
        'Your platelet count is normal, indicating your bloods clotting ability is healthy.'
    )
]

# Insert the data into the table
cursor.executemany("""
INSERT INTO tests (name, aliases, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", tests_to_add)

print(f"{cursor.rowcount} records were inserted into the 'tests' table.")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete and connection closed.")

