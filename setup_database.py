import sqlite3
DATABASE_FILE = 'database/knowledge_base.db'

TESTS_DATA = [
    {
        "name": "Hemoglobin",
        "aliases": "Haemoglobin,Hgb,haemogloBin,HGB,hemogloBin",
        "ref_range_low": 13.2,
        "ref_range_high": 16.6,
        "unit": "g/dL",
        "explanation_low": "Low hemoglobin (anemia) means less oxygen is being carried in your blood, which can cause fatigue.",
        "explanation_high": "High hemoglobin is often a sign of dehydration or other conditions.",
        "explanation_normal": "Your hemoglobin level is normal."
    },
    {
        "name": "WBC",
        "aliases": "WBCs,White Blood Cells,white blood cells,Leukocytes,White Blood Cell Count",
        "ref_range_low": 4.0, 
        "ref_range_high": 11.0,
        "unit": "K/uL",
        "explanation_low": "A low white blood cell count can increase your risk of infection.",
        "explanation_high": "A high white blood cell count usually indicates your body is fighting off an infection.",
        "explanation_normal": "Your white blood cell count is normal."
    },
    {
        "name": "Platelets",
        "aliases": "Thrombocytes,Platelet Count,platelet",
        "ref_range_low": 150,
        "ref_range_high": 450,
        "unit": "K/uL",
        "explanation_low": "A low platelet count can lead to easy bruising and prolonged bleeding.",
        "explanation_high": "A high platelet count can increase the risk of blood clotting.",
        "explanation_normal": "Your platelet count is normal."
    },
    {
        "name": "Red Blood Cell Count",
        "aliases": "RBCs,Red Blood Cells,RBC",
        "ref_range_low": 4.5,
        "ref_range_high": 5.9,
        "unit": "million cells/mcL",
        "explanation_low": "A low RBC count (anemia) can cause fatigue.",
        "explanation_high": "A high RBC count can increase the risk of blood clots.",
        "explanation_normal": "Your count of red blood cells is normal."
    },
    {
        "name": "Sodium",
        "aliases": "Na,Sodum,sodium",
        "ref_range_low": 135,
        "ref_range_high": 145,
        "unit": "mEq/L",
        "explanation_low": "Low sodium can be caused by dehydration or kidney issues.",
        "explanation_high": "High sodium is often related to dehydration or diet.",
        "explanation_normal": "Your sodium level is normal."
    }
]

def create_database():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print(f"--- Connected to {DATABASE_FILE} ---")

        cursor.execute("DROP TABLE IF EXISTS tests")
        print("--- Dropped old 'tests' table. ---")

        cursor.execute("""
        CREATE TABLE tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, aliases TEXT,
            ref_range_low REAL NOT NULL, ref_range_high REAL NOT NULL, unit TEXT NOT NULL,
            explanation_low TEXT, explanation_high TEXT, explanation_normal TEXT
        )
        """)
        print("--- Created new 'tests' table. ---")

        data_to_insert = [
            (
                test['name'], test['aliases'], test['ref_range_low'], test['ref_range_high'],
                test['unit'], test['explanation_low'], test['explanation_high'], test['explanation_normal']
            ) for test in TESTS_DATA
        ]

        cursor.executemany(
            "INSERT INTO tests (name, aliases, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            data_to_insert
        )
        
        print(f"--- Inserted {cursor.rowcount} records. ---")
        conn.commit()
        print("--- Database changes committed. ---")

    except sqlite3.Error as e:
        print(f"!!! Database error: {e} !!!")
    finally:
        if conn:
            conn.close()
            print("--- Database connection closed. ---")

if __name__ == '__main__':
    create_database()
    print(" Database setup is complete. You can now run your Flask app.")

    # To run the database setup script, use the command:
    # python setup_database.py
    

