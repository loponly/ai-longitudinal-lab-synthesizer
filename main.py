"""Main entry point for the AI Longitudinal Lab Report Synthesizer."""
import json

from src.synthesizer import LabDataSynthesizer


def main():
    """Run the example from README."""
    # Example input from README
    example_input = {
        "patient_id": "PT123456",
        "labs": [
            {
                "test_name": "HbA1c",
                "value": 7.2,
                "unit": "%",
                "date": "2023-11-01"
            },
            {
                "test_name": "Creatinine",
                "value": 1.6,
                "unit": "mg/dL",
                "date": "2023-11-01"
            },
            {
                "test_name": "eGFR",
                "value": 54,
                "unit": "mL/min/1.73m2",
                "date": "2023-11-01"
            },
            {
                "test_name": "Fasting Glucose",
                "value": 120,
                "unit": "mg/dL",
                "date": "2023-11-01"
            }
        ]
    }

    print("🧪 AI Longitudinal Lab Report Synthesizer")
    print("=" * 50)

    print("\n📥 Example Input:")
    print(json.dumps(example_input, indent=2))

    # Initialize synthesizer
    synthesizer = LabDataSynthesizer()

    # Process the data
    print("\n🔄 Processing lab data...")
    result = synthesizer.synthesize_to_formats(example_input)

    print("\n📄 Generated Report (Markdown):")
    print("-" * 40)
    print(result["markdown"])

    print("\n\n📊 Expected Output (from README):")
    print("-" * 40)
    expected_output = '''## Patient Summary - ID: PT123456

**Health Domain: Renal**
- **Creatinine**: 1.6 mg/dL ↑ (Normal: 0.6-1.3)
- **eGFR**: 54 mL/min/1.73m² ↓
- **Trend**: 12% decline over 90 days - suggest CKD stage 2

**Endocrinology**
- **HbA1c**: 7.2% ↑ (Pre-Diabetic > 6.5%)
- **Fasting Glucose**: 120 mg/dL ↑

🧠 **Summary**: Patient trending toward early CKD and pre-diabetes. Recommend follow-up testing and nephrology referral.'''

    print(expected_output)

    print("\n\n🔍 Comparison Analysis:")
    print("-" * 40)

    # Compare key elements
    result["markdown"].split("\\n")
    expected_output.split("\\n")

    print("✅ Patient ID match:", "PT123456" in result["markdown"])
    print("✅ Renal domain included:", "Renal" in result["markdown"])
    print("✅ Endocrine domain included:", "Endocrine" in result["markdown"] or "Endocrinology" in result["markdown"])
    print("✅ Creatinine elevated (↑):", "Creatinine" in result["markdown"] and "↑" in result["markdown"])
    print("✅ eGFR decreased (↓):", "eGFR" in result["markdown"] and "↓" in result["markdown"])
    print("✅ HbA1c elevated (↑):", "HbA1c" in result["markdown"] and "↑" in result["markdown"])
    print("✅ Overall summary present:", "Summary" in result["markdown"] and ("CKD" in result["markdown"] or "diabetes" in result["markdown"]))

    return result


if __name__ == "__main__":
    main()
