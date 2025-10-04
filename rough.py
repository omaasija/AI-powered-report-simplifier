# Step 1: Set the Request Method and URL

#     Open a new tab in Postman.

#     Change the HTTP Method from GET to POST.

#     In the URL bar, enter the address for your file upload endpoint:
#     http://127.0.0.1:5000/simplify-file

# Step 2: Configure the Request Body for File Upload

#     Click on the Body tab below the URL bar.

#     Select the form-data radio button. This is the correct type for sending files.

# Step 3: Attach the File

#     A table of Key-Value pairs will appear. In the first row, under the KEY column, type the name your Flask app is expecting: report_file. (This must be spelled exactly right).

#     Hover your mouse over the KEY cell you just typed in. On the right side, a dropdown menu will appear that says "Text". Click it and select "File".

#     The VALUE column will now change to a button that says "Select Files". Click this button.

#     A file browser window will open. Navigate to and select the .txt or image file (e.g., sample_report.txt or report_image.png) you want to upload.

{
    "name": "Total Cholesterol",
    "aliases": "cholesterol",
    "ref_range_low": 100,
    "ref_range_high": 200,
    "unit": "mg/dL",
    "explanation_low": "While very low cholesterol is uncommon, it can be a sign of other health issues.",
    "explanation_high": "High total cholesterol can increase your risk of heart disease.",
    "explanation_normal": "Your total cholesterol level is within the desirable range."
}

{
    "name": "LDL Cholesterol",
    "aliases": "ldl, ldl-c",
    "ref_range_low": 0,
    "ref_range_high": 100,
    "unit": "mg/dL",
    "explanation_low": "A low LDL level is excellent and desirable for heart health.",
    "explanation_high": "High LDL cholesterol is a major risk factor for plaque buildup in arteries.",
    "explanation_normal": "Your LDL (bad) cholesterol level is optimal."
}

{
    "name": "HDL Cholesterol",
    "aliases": "hdl, hdl-c",
    "ref_range_low": 40,
    "ref_range_high": 100,
    "unit": "mg/dL",
    "explanation_low": "Low HDL cholesterol can increase your risk of heart disease. Higher levels are generally better.",
    "explanation_high": "A high HDL level is considered protective against heart disease.",
    "explanation_normal": "Your HDL (good) cholesterol level is in a healthy range."
}
{
    "name": "HDL Cholesterol",
    "aliases": "hdl, hdl-c",
    "ref_range_low": 40,
    "ref_range_high": 100,
    "unit": "mg/dL",
    "explanation_low": "Low HDL cholesterol can increase your risk of heart disease. Higher levels are generally better.",
    "explanation_high": "A high HDL level is considered protective against heart disease.",
    "explanation_normal": "Your HDL (good) cholesterol level is in a healthy range."
}

{
    "name": "Triglycerides",
    "aliases": "trigs",
    "ref_range_low": 0,
    "ref_range_high": 150,
    "unit": "mg/dL",
    "explanation_low": "Low triglyceride levels are generally not a cause for concern.",
    "explanation_high": "High triglycerides can be a risk factor for heart disease and pancreatitis.",
    "explanation_normal": "Your triglyceride level is normal."
}

{
    "name": "Red Blood Cell Count",
    "aliases": "RBCs, Red Blood Cells, RBC",
    "ref_range_low": 4.5,
    "ref_range_high": 5.9,
    "unit": "million cells/mcL",
    "explanation_low": "A low RBC count (anemia) means your body may not be getting enough oxygen, which can cause fatigue and weakness.",
    "explanation_high": "A high RBC count can increase the risk of blood clots and may be a sign of dehydration or other medical conditions.",
    "explanation_normal": "Your count of oxygen-carrying red blood cells is in the normal range."
}

{
    "name": "MCV",
    "aliases": "MCV",
    "ref_range_low": 80,
    "ref_range_high": 100,
    "unit": "fL",
    "explanation_low": "Low MCV means your red blood cells are smaller than average, which can be a sign of iron-deficiency anemia.",
    "explanation_high": "High MCV means your red blood cells are larger than average, often caused by a vitamin B12 or folate deficiency.",
    "explanation_normal": "The average size of your red blood cells is within the normal range."
}

{
    "name": "Platelets",
    "aliases": "Thrombocytes, Platelet Count",
    "ref_range_low": 150000,
    "ref_range_high": 450000,
    "unit": "/uL",
    "explanation_low": "A low platelet count (thrombocytopenia) can lead to easy bruising and prolonged bleeding from cuts.",
    "explanation_high": "A high platelet count (thrombocytosis) can increase the risk of forming unnecessary blood clots.",
    "explanation_normal": "Your platelet count is normal, indicating your blood's ability to form clots is healthy."
}

# rbc:  44.44
# wbc : 33.44

# Hemoglobin: 77
# Na : 55