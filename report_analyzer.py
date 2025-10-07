import re
import sqlite3
from database_utils import get_db_connection

def normalize_tests(report_text):
   #take raw report text and return a list of normalized test objects

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

    normalized_tests = []
    raw_test_lines = []
    report_lines = report_text.split('\n')
    processed_lines = set()

    for i, line in enumerate(report_lines):
        if i in processed_lines: continue

        for keyword, test_info in knowledge_base.items():
            if keyword and keyword in line.lower():
                match = re.search(f'{re.escape(keyword)}[^\\d]*([\\d\\.]+)', line, re.IGNORECASE)
                
                if match:
                    raw_test_lines.append(line.strip())
                    value = float(match.group(1))
                    status = 'normal'
                    ref_low, ref_high = test_info["ref_range_low"], test_info["ref_range_high"]
                    
                    if value < ref_low: status = 'low'
                    elif value > ref_high: status = 'high'
                    
                    normalized_test_obj = {
                        "name": test_info["name"], "value": value, "unit": test_info["unit"], 
                        "status": status, "ref_range": { "low": ref_low, "high": ref_high }
                    }
                    normalized_tests.append(normalized_test_obj)
                    
                    processed_lines.add(i)
                    break 
    conn.close()
    return raw_test_lines, normalized_tests, 1.0 # Return confidence placeholder

def generate_summary(normalized_tests):
    # Generate a summary string and explanations for abnormal tests
    summary_parts = []
    explanations = []
    
    conn = get_db_connection()
    cursor = conn.cursor()

    for test in normalized_tests:
        if test['status'] != 'normal':
            # Create the summary part with lowercase, e.g., "low hemoglobin"
            summary_parts.append(f"{test['status']} {test['name'].lower()}")
            
            # Fetch the explanation for this specific test
            cursor.execute("SELECT explanation_low, explanation_high FROM tests WHERE name = ?", (test['name'],))
            explanation_info = cursor.fetchone()
            if explanation_info:
                explanation_key = f"explanation_{test['status']}"
                explanations.append(explanation_info[explanation_key])

    conn.close()
    
    # Join the parts and capitalize the first letter, e.g., "Low hemoglobin and high wbc."
    summary_text = " and ".join(summary_parts)
    if summary_text:
        summary_text = summary_text[0].upper() + summary_text[1:] + "."
    else:
        summary_text = "All test results are within the normal range."
    
    return {
        "summary": summary_text,
        "explanations": explanations
    }

def generate_final_output(normalized_tests):
   # Generate the final output
    summary_obj = generate_summary(normalized_tests)
    
    # Filter out normal tests for the final output
    abnormal_tests = [test for test in normalized_tests if test['status'] != 'normal']
    
    return {
        "tests": abnormal_tests,
        "summary": summary_obj['summary'],
        "status": "ok"
    }

