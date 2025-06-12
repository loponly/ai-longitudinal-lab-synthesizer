"""Integration tests for the complete lab synthesizer system."""
import json
import time

import pytest

from src.synthesizer import LabDataSynthesizer


class TestIntegration:
    """Integration tests for the complete system."""

    @pytest.fixture
    def readme_example_input(self):
        """The exact example input from the README."""
        return {
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

    def test_readme_example_end_to_end(self, readme_example_input):
        """Test the complete pipeline with README example."""
        synthesizer = LabDataSynthesizer(use_mock=True)
        results = synthesizer.synthesize_to_formats(readme_example_input)

        # Check that all formats are generated
        assert "markdown" in results
        assert "latex" in results
        assert "json" in results
        assert "patient_summary" in results

        markdown_report = results["markdown"]

        # Check key elements match expected output
        assert "PT123456" in markdown_report
        assert "Renal" in markdown_report
        assert "Endocrine" in markdown_report or "Endocrinology" in markdown_report
        assert "Creatinine" in markdown_report
        assert "HbA1c" in markdown_report
        assert "eGFR" in markdown_report
        assert "Fasting Glucose" in markdown_report

        # Check status indicators
        assert "↑" in markdown_report  # Should have elevated values
        assert "↓" in markdown_report  # Should have decreased eGFR

        # Check reference ranges
        assert "Normal:" in markdown_report
        assert "0.6-1.3" in markdown_report  # Creatinine range
        assert "4.0-5.6" in markdown_report  # HbA1c range

        # Check trends and recommendations
        assert ("CKD" in markdown_report or "kidney" in markdown_report)
        assert ("diabetes" in markdown_report or "glucose" in markdown_report)

    def test_comprehensive_lab_panel(self):
        """Test with a comprehensive lab panel covering multiple domains."""
        comprehensive_input = {
            "patient_id": "PT999999",
            "labs": [
                # Renal
                {"test_name": "Creatinine", "value": 2.1, "unit": "mg/dL", "date": "2023-11-01"},
                {"test_name": "eGFR", "value": 35, "unit": "mL/min/1.73m2", "date": "2023-11-01"},
                {"test_name": "BUN", "value": 45, "unit": "mg/dL", "date": "2023-11-01"},

                # Endocrine
                {"test_name": "HbA1c", "value": 9.2, "unit": "%", "date": "2023-11-01"},
                {"test_name": "Fasting Glucose", "value": 220, "unit": "mg/dL", "date": "2023-11-01"},

                # Lipid
                {"test_name": "Total Cholesterol", "value": 280, "unit": "mg/dL", "date": "2023-11-01"},
                {"test_name": "HDL Cholesterol", "value": 25, "unit": "mg/dL", "date": "2023-11-01"},
                {"test_name": "LDL Cholesterol", "value": 180, "unit": "mg/dL", "date": "2023-11-01"},

                # Hematology
                {"test_name": "Hemoglobin", "value": 8.5, "unit": "g/dL", "date": "2023-11-01"},
                {"test_name": "Hematocrit", "value": 25, "unit": "%", "date": "2023-11-01"},

                # Liver
                {"test_name": "ALT", "value": 85, "unit": "U/L", "date": "2023-11-01"},
                {"test_name": "AST", "value": 95, "unit": "U/L", "date": "2023-11-01"},

                # Thyroid
                {"test_name": "TSH", "value": 12.5, "unit": "mIU/L", "date": "2023-11-01"}
            ]
        }

        synthesizer = LabDataSynthesizer(use_mock=True)
        results = synthesizer.synthesize_to_formats(comprehensive_input)

        markdown_report = results["markdown"]
        patient_summary = results["patient_summary"]

        # Should have multiple health domains
        domains = [summary.domain.value for summary in patient_summary.health_summaries]
        expected_domains = ["Renal", "Endocrine", "Lipid", "Hematology", "Liver", "Thyroid"]

        for domain in expected_domains:
            assert domain in domains, f"Missing domain: {domain}"

        # Check that all abnormal values are flagged
        assert markdown_report.count("↑") >= 8  # Many elevated values
        assert markdown_report.count("↓") >= 2  # Some decreased values

        # Check comprehensive summary
        assert len(patient_summary.overall_summary) > 50  # Should be detailed

    def test_normal_values_integration(self):
        """Test integration with all normal lab values."""
        normal_input = {
            "patient_id": "PT555555",
            "labs": [
                {"test_name": "HbA1c", "value": 5.2, "unit": "%", "date": "2023-11-01"},
                {"test_name": "Creatinine", "value": 1.0, "unit": "mg/dL", "date": "2023-11-01"},
                {"test_name": "eGFR", "value": 85, "unit": "mL/min/1.73m2", "date": "2023-11-01"},
                {"test_name": "Fasting Glucose", "value": 90, "unit": "mg/dL", "date": "2023-11-01"},
                {"test_name": "Total Cholesterol", "value": 180, "unit": "mg/dL", "date": "2023-11-01"}
            ]
        }

        synthesizer = LabDataSynthesizer(use_mock=True)
        results = synthesizer.synthesize_to_formats(normal_input)

        markdown_report = results["markdown"]
        patient_summary = results["patient_summary"]

        # Should have minimal abnormal indicators
        assert markdown_report.count("↑") <= 1
        assert markdown_report.count("↓") <= 1

        # Overall summary should indicate stability
        assert ("stable" in patient_summary.overall_summary.lower() or
                "normal" in patient_summary.overall_summary.lower())

    def test_error_handling_invalid_date(self):
        """Test error handling with invalid date format."""
        invalid_input = {
            "patient_id": "PT666666",
            "labs": [
                {"test_name": "HbA1c", "value": 7.2, "unit": "%", "date": "invalid-date"}
            ]
        }

        synthesizer = LabDataSynthesizer(use_mock=True)

        with pytest.raises(ValueError, match="Invalid date format"):
            synthesizer.synthesize_to_formats(invalid_input)

    def test_json_serialization_integration(self):
        """Test that JSON serialization works end-to-end."""
        input_data = {
            "patient_id": "PT777777",
            "labs": [
                {"test_name": "HbA1c", "value": 6.8, "unit": "%", "date": "2023-11-01"},
                {"test_name": "Creatinine", "value": 1.4, "unit": "mg/dL", "date": "2023-11-01"}
            ]
        }

        synthesizer = LabDataSynthesizer(use_mock=True)
        results = synthesizer.synthesize_to_formats(input_data)

        # Test that JSON result can be serialized
        json_report = results["json"]
        json_string = json.dumps(json_report, indent=2)

        # And deserialized
        reconstructed = json.loads(json_string)

        assert reconstructed["patient_id"] == "PT777777"
        assert len(reconstructed["health_summaries"]) >= 1

        # Check that enum values are properly converted
        for summary in reconstructed["health_summaries"]:
            assert isinstance(summary["domain"], str)
            assert summary["domain"] in ["Renal", "Endocrine", "Lipid", "Hematology", "Liver", "Thyroid", "Other"]

    def test_performance_with_large_dataset(self):
        """Test performance with a larger dataset."""
        # Create a larger dataset
        large_input = {
            "patient_id": "PT888888",
            "labs": []
        }

        # Add 50 lab results
        test_names = ["HbA1c", "Creatinine", "eGFR", "Fasting Glucose", "Total Cholesterol"]
        for i in range(50):
            large_input["labs"].append({
                "test_name": test_names[i % len(test_names)],
                "value": 100 + (i % 50),
                "unit": "mg/dL",
                "date": "2023-11-01"
            })

        synthesizer = LabDataSynthesizer(use_mock=True)

        start_time = time.time()
        results = synthesizer.synthesize_to_formats(large_input)
        end_time = time.time()

        # Should complete in reasonable time (< 5 seconds)
        assert (end_time - start_time) < 5.0

        # Should still produce valid output
        assert "PT888888" in results["markdown"]
        assert len(results["patient_summary"].health_summaries) >= 1
