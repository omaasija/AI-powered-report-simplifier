import re
import sqlite3
from database_utils import get_db_connection

def process_report_text(report_text):
    """
    The main analysis engine. Takes raw text, finds known medical tests using a
    database-driven keyword map, calculates their status, and returns a structured result.

    Args:
        report_text (str): The raw text extracted from a report.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    normalized_tests, summary_parts = [], []
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        knowledge_base = {}
        cursor.execute("SELECT * FROM tests")
        for test_info in cursor.fetchall():
            canonical_name = test_info['name']
            knowledge_base[canonical_name.lower()] = dict(test_info)
            if test_info['aliases']:
                for alias in test_info['aliases'].split(','):
                    knowledge_base[alias.lower().strip()] = dict(test_info)

        report_lines = report_text.split('\n')
        processed_lines = set()

        for i, line in enumerate(report_lines):
            if i in processed_lines: continue

            for keyword, test_info in knowledge_base.items():
                # Ensure the keyword is not empty before creating a regex from it
                if not keyword: continue

                if keyword in line.lower():
                    # Use a context-aware regex to find the number *after* the keyword
                    match = re.search(f'{re.escape(keyword)}[^\\d]*([\\d\\.]+)', line, re.IGNORECASE)
                    
                    if match:
                        value = float(match.group(1))
                        status = 'normal'
                        ref_low, ref_high = test_info["ref_range_low"], test_info["ref_range_high"]
                        
                        if value < ref_low: status = 'low'
                        elif value > ref_high: status = 'high'
                        
                        if status != 'normal':
                            explanation_key = f"explanation_{status}"
                            test_output = {
                                "name": test_info["name"], "value": value, "unit": test_info["unit"], 
                                "status": status, "ref_range": { "low": ref_low, "high": ref_high }, 
                                "explanation": test_info[explanation_key]
                            }
                            normalized_tests.append(test_output)
                            summary_parts.append(f"{status.capitalize()} {test_info['name']}")
                        
                        processed_lines.add(i)
                        break

    except sqlite3.Error as e:
        print(f"Database error during processing: {e}")
        return {"status": "error", "message": "A database error occurred."}
    finally:
        if conn:
            conn.close()

    if not summary_parts:
        return {"status": "ok", "message": "No abnormal test results were found from the list of known tests."}
    
    return {
        "status": "ok", 
        "summary": "Your report shows: " + " and ".join(summary_parts) + ".",
        "tests": normalized_tests
    }

