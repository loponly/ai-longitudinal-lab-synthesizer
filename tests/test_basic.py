"""Basic functionality tests."""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import LabResult
from src.synthesizer import LabDataSynthesizer


def test_lab_result_creation():
    """Test basic lab result creation."""
    lab = LabResult("HbA1c", 7.2, "%", "2023-11-01")
    assert lab.test_name == "HbA1c"
    assert lab.value == 7.2
    assert lab.unit == "%"
    assert lab.date == "2023-11-01"

def test_synthesizer_creation():
    """Test synthesizer creation."""
    synthesizer = LabDataSynthesizer(use_mock=True)
    assert synthesizer is not None

def test_readme_example():
    """Test the README example end-to-end."""
    example_input = {
        "patient_id": "PT123456",
        "labs": [
            {"test_name": "HbA1c", "value": 7.2, "unit": "%", "date": "2023-11-01"},
            {"test_name": "Creatinine", "value": 1.6, "unit": "mg/dL", "date": "2023-11-01"},
            {"test_name": "eGFR", "value": 54, "unit": "mL/min/1.73m2", "date": "2023-11-01"},
            {"test_name": "Fasting Glucose", "value": 120, "unit": "mg/dL", "date": "2023-11-01"}
        ]
    }

    synthesizer = LabDataSynthesizer(use_mock=True)
    results = synthesizer.synthesize_to_formats(example_input)

    # Check basic structure
    assert "markdown" in results
    assert "PT123456" in results["markdown"]
    assert "Renal" in results["markdown"]
    assert ("Endocrine" in results["markdown"] or "Endocrinology" in results["markdown"])
    assert "↑" in results["markdown"]  # Should have elevated indicators
    assert "↓" in results["markdown"]  # Should have decreased indicators
