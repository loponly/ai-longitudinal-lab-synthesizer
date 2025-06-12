"""Test utilities and fixtures for the lab synthesizer tests."""
import pytest

from src.models import HealthDomain, LabResult, PatientData


@pytest.fixture
def sample_lab_result():
    """Sample lab result for testing."""
    return LabResult(
        test_name="Creatinine",
        value=1.6,
        unit="mg/dL",
        date="2023-11-01"
    )


@pytest.fixture
def sample_patient_data():
    """Sample patient data from README example."""
    return PatientData(
        patient_id="PT123456",
        labs=[
            LabResult(test_name="HbA1c", value=7.2, unit="%", date="2023-11-01"),
            LabResult(test_name="Creatinine", value=1.6, unit="mg/dL", date="2023-11-01"),
            LabResult(test_name="eGFR", value=54, unit="mL/min/1.73m2", date="2023-11-01"),
            LabResult(test_name="Fasting Glucose", value=120, unit="mg/dL", date="2023-11-01")
        ]
    )


@pytest.fixture
def normal_lab_results():
    """Normal lab results for testing."""
    return [
        LabResult(test_name="HbA1c", value=5.2, unit="%", date="2023-11-01"),
        LabResult(test_name="Creatinine", value=1.0, unit="mg/dL", date="2023-11-01"),
        LabResult(test_name="eGFR", value=85, unit="mL/min/1.73m2", date="2023-11-01")
    ]


@pytest.fixture
def abnormal_lab_results():
    """Abnormal lab results for testing."""
    return [
        LabResult(test_name="HbA1c", value=9.5, unit="%", date="2023-11-01"),
        LabResult(test_name="Creatinine", value=2.8, unit="mg/dL", date="2023-11-01"),
        LabResult(test_name="eGFR", value=25, unit="mL/min/1.73m2", date="2023-11-01")
    ]
