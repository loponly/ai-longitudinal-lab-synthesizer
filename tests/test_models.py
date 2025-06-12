"""Tests for data models."""

import pytest

from src.models import HealthDomain, LabResult, PatientData, ReferenceRange


class TestLabResult:
    """Test LabResult model."""

    def test_lab_result_creation(self):
        """Test basic lab result creation."""
        lab = LabResult(
            test_name="Glucose",
            value=120.5,
            unit="mg/dL",
            date="2023-11-01"
        )

        assert lab.test_name == "Glucose"
        assert lab.value == 120.5
        assert lab.unit == "mg/dL"
        assert lab.date == "2023-11-01"
        assert lab.loinc_code is None
        assert lab.reference_range is None
        assert lab.health_domain is None

    def test_lab_result_invalid_date(self):
        """Test lab result with invalid date format."""
        with pytest.raises(ValueError, match="Invalid date format"):
            LabResult(
                test_name="Glucose",
                value=120.5,
                unit="mg/dL",
                date="invalid-date"
            )

    def test_lab_result_with_optional_fields(self):
        """Test lab result with all optional fields."""
        lab = LabResult(
            test_name="HbA1c",
            value=7.2,
            unit="%",
            date="2023-11-01",
            loinc_code="4548-4",
            reference_range="Normal: 4.0-5.6",
            health_domain=HealthDomain.ENDOCRINE
        )

        assert lab.loinc_code == "4548-4"
        assert lab.reference_range == "Normal: 4.0-5.6"
        assert lab.health_domain == HealthDomain.ENDOCRINE


class TestPatientData:
    """Test PatientData model."""

    def test_patient_data_creation(self):
        """Test patient data creation with lab results."""
        labs = [
            LabResult("HbA1c", 7.2, "%", "2023-11-01"),
            LabResult("Glucose", 120, "mg/dL", "2023-11-01")
        ]

        patient = PatientData(patient_id="PT123", labs=labs)

        assert patient.patient_id == "PT123"
        assert len(patient.labs) == 2
        assert all(isinstance(lab, LabResult) for lab in patient.labs)

    def test_patient_data_dict_conversion(self):
        """Test patient data creation from dict format."""
        lab_dicts = [
            {"test_name": "HbA1c", "value": 7.2, "unit": "%", "date": "2023-11-01"},
            {"test_name": "Glucose", "value": 120, "unit": "mg/dL", "date": "2023-11-01"}
        ]

        patient = PatientData(patient_id="PT123", labs=lab_dicts)

        assert len(patient.labs) == 2
        assert all(isinstance(lab, LabResult) for lab in patient.labs)
        assert patient.labs[0].test_name == "HbA1c"


class TestReferenceRange:
    """Test ReferenceRange model."""

    def test_reference_range_normal_value(self):
        """Test reference range with normal value."""
        ref_range = ReferenceRange("Glucose", 70, 140, "mg/dL")

        assert ref_range.is_normal(100) is True
        assert ref_range.get_status(100) == ""

    def test_reference_range_high_value(self):
        """Test reference range with high value."""
        ref_range = ReferenceRange("Glucose", 70, 140, "mg/dL")

        assert ref_range.is_normal(200) is False
        assert ref_range.get_status(200) == "↑"

    def test_reference_range_low_value(self):
        """Test reference range with low value."""
        ref_range = ReferenceRange("Glucose", 70, 140, "mg/dL")

        assert ref_range.is_normal(50) is False
        assert ref_range.get_status(50) == "↓"

    def test_reference_range_no_min(self):
        """Test reference range with no minimum."""
        ref_range = ReferenceRange("HDL", None, 200, "mg/dL")

        assert ref_range.is_normal(50) is True
        assert ref_range.is_normal(250) is False
        assert ref_range.get_status(250) == "↑"

    def test_reference_range_no_max(self):
        """Test reference range with no maximum."""
        ref_range = ReferenceRange("eGFR", 60, None, "mL/min/1.73m2")

        assert ref_range.is_normal(80) is True
        assert ref_range.is_normal(40) is False
        assert ref_range.get_status(40) == "↓"


class TestHealthDomain:
    """Test HealthDomain enum."""

    def test_health_domain_values(self):
        """Test health domain enum values."""
        assert HealthDomain.RENAL.value == "Renal"
        assert HealthDomain.ENDOCRINE.value == "Endocrine"
        assert HealthDomain.CARDIOVASCULAR.value == "Cardiovascular"
        assert HealthDomain.OTHER.value == "Other"

    def test_health_domain_membership(self):
        """Test health domain enum membership."""
        domains = list(HealthDomain)
        assert HealthDomain.RENAL in domains
        assert HealthDomain.ENDOCRINE in domains
        assert len(domains) >= 8  # Should have at least 8 domains
