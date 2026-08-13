"""
Medical reference ranges used by the AI Medical Report Analyzer.

These are simplified reference values for demonstration purposes.
In real hospitals, ranges vary depending on:
- Age
- Sex
- Pregnancy
- Laboratory standards
"""

MEDICAL_RANGES = {

    "Hemoglobin": {
        "low": 13.5,
        "high": 17.5,
        "unit": "g/dL"
    },

    "Glucose": {
        "low": 70,
        "high": 99,
        "unit": "mg/dL"
    },

    "Vitamin D": {
        "low": 20,
        "high": 50,
        "unit": "ng/mL"
    },

    "Cholesterol": {
        "low": 0,
        "high": 200,
        "unit": "mg/dL"
    }

}