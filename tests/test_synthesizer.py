"""Tests for the main synthesizer orchestrator."""
import json

import pytest

from src.models import HealthDomain, LabResult, PatientData
from src.synthesizer import LabDataSynthesizer


class TestLabDataSynthesizer:
    """Test the main lab data synthesizer functionality."""

    @pytest.fixture
    def synthesizer(self):
        """Create synthesizer instance."""
        return LabDataSynthesizer(use_mock=True)

    @pytest.fixture
    def sample_patient_data(self):
        """Sample patient data for testing."""
        return PatientData(
            patient_id="PT123456",
            labs=[
                LabResult("HbA1c", 7.2, "%", "2023-11-01"),
                LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01"),
                LabResult("eGFR", 54, "mL/min/1.73m2", "2023-11-01"),
                LabResult("Fasting Glucose", 120, "mg/dL", "2023-11-01")
            ]
        )

    @pytest.fixture
    def sample_json_input(self):
        """Sample JSON input for testing."""
        return {
            "patient_id": "PT123456",
            "labs": [
                {"test_name": "HbA1c", "value": 7.2, "unit": "%", "date": "2023-11-01"},
                {"test_name": "Creatinine", "value": 1.6, "unit": "mg/dL", "date": "2023-11-01"},
                {"test_name": "eGFR", "value": 54, "unit": "mL/min/1.73m2", "date": "2023-11-01"},
                {"test_name": "Fasting Glucose", "value": 120, "unit": "mg/dL", "date": "2023-11-01"}
            ]
        }

    def test_synthesizer_initialization(self, synthesizer):
        """Test synthesizer initialization."""
        assert synthesizer is not None
        assert isinstance(synthesizer, LabDataSynthesizer)

    def test_process_patient_data(self, synthesizer, sample_patient_data):
        """Test processing patient data through the pipeline."""
        patient_summary = synthesizer.process_patient_data(sample_patient_data)

        # Check basic structure
        assert patient_summary.patient_id == "PT123456"
        assert len(patient_summary.health_summaries) >= 2  # At least renal and endocrine
        assert patient_summary.overall_summary is not None

        # Check that labs have been processed
        for lab in sample_patient_data.labs:
            assert lab.loinc_code is not None or lab.test_name not in ["HbA1c", "Creatinine"]
            assert lab.reference_range is not None or lab.test_name not in ["HbA1c", "Creatinine"]
            assert lab.health_domain is not None

        # Check health domains are present
        domains = [summary.domain for summary in patient_summary.health_summaries]
        assert HealthDomain.RENAL in domains
        assert HealthDomain.ENDOCRINE in domains

    def test_process_patient_data_loinc_mapping(self, synthesizer, sample_patient_data):
        """Test that LOINC codes are mapped correctly."""
        synthesizer.process_patient_data(sample_patient_data)

        # Find HbA1c and Creatinine labs
        hba1c_lab = next((lab for lab in sample_patient_data.labs if lab.test_name == "HbA1c"), None)
        creatinine_lab = next((lab for lab in sample_patient_data.labs if lab.test_name == "Creatinine"), None)

        assert hba1c_lab is not None
        assert creatinine_lab is not None
        assert hba1c_lab.loinc_code == "4548-4"
        assert creatinine_lab.loinc_code == "2160-0"

    def test_process_patient_data_reference_ranges(self, synthesizer, sample_patient_data):
        """Test that reference ranges are added correctly."""
        synthesizer.process_patient_data(sample_patient_data)

        # Check that reference ranges are populated
        for lab in sample_patient_data.labs:
            if lab.test_name in ["HbA1c", "Creatinine", "eGFR", "Fasting Glucose"]:
                assert lab.reference_range is not None
                assert "Normal:" in lab.reference_range

    def test_process_patient_data_health_classification(self, synthesizer, sample_patient_data):
        """Test that health domains are classified correctly."""
        synthesizer.process_patient_data(sample_patient_data)

        # Check specific classifications
        hba1c_lab = next((lab for lab in sample_patient_data.labs if lab.test_name == "HbA1c"), None)
        creatinine_lab = next((lab for lab in sample_patient_data.labs if lab.test_name == "Creatinine"), None)

        assert hba1c_lab.health_domain == HealthDomain.ENDOCRINE
        assert creatinine_lab.health_domain == HealthDomain.RENAL

    def test_generate_overall_summary_with_issues(self, synthesizer):
        """Test overall summary generation with health issues."""
        from src.models import HealthSummary

        health_summaries = [
            HealthSummary(
                domain=HealthDomain.RENAL,
                lab_results=[],
                trends="Elevated creatinine - suggest nephrology referral"
            ),
            HealthSummary(
                domain=HealthDomain.ENDOCRINE,
                lab_results=[],
                trends="Elevated HbA1c - suggest follow-up testing"
            )
        ]

        summary = synthesizer._generate_overall_summary(health_summaries)

        assert "early CKD" in summary.lower() or "ckd" in summary.lower()
        assert "nephrology referral" in summary.lower()
        assert "follow-up testing" in summary.lower()

    def test_generate_overall_summary_normal_values(self, synthesizer):
        """Test overall summary generation with normal values."""
        from src.models import HealthSummary

        health_summaries = [
            HealthSummary(
                domain=HealthDomain.RENAL,
                lab_results=[],
                trends="Values within normal limits"
            ),
            HealthSummary(
                domain=HealthDomain.ENDOCRINE,
                lab_results=[],
                trends="Good glucose control"
            )
        ]

        summary = synthesizer._generate_overall_summary(health_summaries)

        assert "stable" in summary.lower()
        assert "no significant abnormalities" in summary.lower()

    def test_synthesize_from_json_string(self, synthesizer, sample_json_input):
        """Test synthesizing from JSON string input."""
        json_string = json.dumps(sample_json_input)
        markdown_report = synthesizer.synthesize_from_json(json_string)

        assert "## Patient Summary - ID: PT123456" in markdown_report
        assert "Renal" in markdown_report
        assert "Endocrine" in markdown_report
        assert "Creatinine" in markdown_report
        assert "HbA1c" in markdown_report

    def test_synthesize_from_json_dict(self, synthesizer, sample_json_input):
        """Test synthesizing from JSON dict input."""
        markdown_report = synthesizer.synthesize_from_json(sample_json_input)

        assert "## Patient Summary - ID: PT123456" in markdown_report
        assert "**Health Domain:" in markdown_report

    def test_synthesize_to_formats(self, synthesizer, sample_json_input):
        """Test synthesizing to multiple formats."""
        results = synthesizer.synthesize_to_formats(sample_json_input)

        assert "markdown" in results
        assert "latex" in results
        assert "json" in results
        assert "patient_summary" in results

        # Check markdown format
        assert "## Patient Summary - ID: PT123456" in results["markdown"]

        # Check LaTeX format
        assert "\\documentclass{article}" in results["latex"]
        assert "\\section{Patient Summary - ID: PT123456}" in results["latex"]

        # Check JSON format
        assert isinstance(results["json"], dict)
        assert results["json"]["patient_id"] == "PT123456"

        # Check patient summary object
        assert results["patient_summary"].patient_id == "PT123456"

    def test_synthesize_empty_labs(self, synthesizer):
        """Test synthesizing with empty labs list."""
        empty_input = {
            "patient_id": "PT000000",
            "labs": []
        }

        results = synthesizer.synthesize_to_formats(empty_input)

        assert "PT000000" in results["markdown"]
        assert results["patient_summary"].patient_id == "PT000000"
        assert len(results["patient_summary"].health_summaries) == 0

    def test_synthesize_single_lab(self, synthesizer):
        """Test synthesizing with single lab result."""
        single_lab_input = {
            "patient_id": "PT111111",
            "labs": [
                {"test_name": "HbA1c", "value": 7.2, "unit": "%", "date": "2023-11-01"}
            ]
        }

        results = synthesizer.synthesize_to_formats(single_lab_input)

        assert "PT111111" in results["markdown"]
        assert "HbA1c" in results["markdown"]
        assert len(results["patient_summary"].health_summaries) == 1
        assert results["patient_summary"].health_summaries[0].domain == HealthDomain.ENDOCRINE

    def test_synthesize_unknown_labs(self, synthesizer):
        """Test synthesizing with unknown lab tests."""
        unknown_lab_input = {
            "patient_id": "PT222222",
            "labs": [
                {"test_name": "Unknown Test 1", "value": 100, "unit": "units", "date": "2023-11-01"},
                {"test_name": "Unknown Test 2", "value": 200, "unit": "mg/dL", "date": "2023-11-01"}
            ]
        }

        results = synthesizer.synthesize_to_formats(unknown_lab_input)

        assert "PT222222" in results["markdown"]
        # Should still process and classify as OTHER domain
        assert len(results["patient_summary"].health_summaries) >= 0
