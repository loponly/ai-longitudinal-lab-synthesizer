"""Simple test to verify the system works."""
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

def test_basic_import():
    """Test that we can import the main modules."""
    from src.models import LabResult
    from src.synthesizer import LabDataSynthesizer

    # Create a simple lab result
    lab = LabResult("HbA1c", 7.2, "%", "2023-11-01")
    assert lab.test_name == "HbA1c"
    assert lab.value == 7.2

    # Create synthesizer
    synthesizer = LabDataSynthesizer()
    assert synthesizer is not None

    print("✅ Basic imports and creation work!")

if __name__ == "__main__":
    test_basic_import()
