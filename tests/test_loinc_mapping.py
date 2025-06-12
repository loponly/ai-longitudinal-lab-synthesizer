"""Tests for LOINC mapping and biomarker normalization."""
import pytest
from src.loinc_mapping import LOINCMapper, BiomarkerNormalizer
from src.models import LabResult, ReferenceRange


class TestLOINCMapper:
    """Test LOINC code mapping functionality."""
    
    def test_exact_match_loinc_code(self):
        """Test exact match LOINC code lookup."""
        code = LOINCMapper.get_loinc_code("HbA1c")
        assert code == "4548-4"
        
        code = LOINCMapper.get_loinc_code("Creatinine")
        assert code == "2160-0"
    
    def test_case_insensitive_loinc_code(self):
        """Test case-insensitive LOINC code lookup."""
        code = LOINCMapper.get_loinc_code("hba1c")
        assert code == "4548-4"
        
        code = LOINCMapper.get_loinc_code("CREATININE")
        assert code == "2160-0"
    
    def test_unknown_test_loinc_code(self):
        """Test unknown test returns None."""
        code = LOINCMapper.get_loinc_code("Unknown Test")
        assert code is None
    
    def test_map_lab_result(self):
        """Test mapping LOINC code to lab result."""
        lab = LabResult("HbA1c", 7.2, "%", "2023-11-01")
        assert lab.loinc_code is None
        
        mapped_lab = LOINCMapper.map_lab_result(lab)
        assert mapped_lab.loinc_code == "4548-4"
        assert mapped_lab is lab  # Should modify in place
    
    def test_map_unknown_lab_result(self):
        """Test mapping unknown lab result."""
        lab = LabResult("Unknown Test", 100, "units", "2023-11-01")
        mapped_lab = LOINCMapper.map_lab_result(lab)
        assert mapped_lab.loinc_code is None


class TestBiomarkerNormalizer:
    """Test biomarker normalization functionality."""
    
    def test_get_reference_range_exact_match(self):
        """Test exact match reference range lookup."""
        ref_range = BiomarkerNormalizer.get_reference_range("HbA1c")
        assert ref_range is not None
        assert ref_range.test_name == "HbA1c"
        assert ref_range.min_value == 4.0
        assert ref_range.max_value == 5.6
        assert ref_range.unit == "%"
    
    def test_get_reference_range_case_insensitive(self):
        """Test case-insensitive reference range lookup."""
        ref_range = BiomarkerNormalizer.get_reference_range("hba1c")
        assert ref_range is not None
        assert ref_range.test_name == "HbA1c"
    
    def test_get_reference_range_unknown(self):
        """Test unknown test returns None."""
        ref_range = BiomarkerNormalizer.get_reference_range("Unknown Test")
        assert ref_range is None
    
    def test_normalize_lab_result_with_range(self):
        """Test normalizing lab result with reference range."""
        lab = LabResult("HbA1c", 7.2, "%", "2023-11-01")
        normalized_lab = BiomarkerNormalizer.normalize_lab_result(lab)
        
        assert normalized_lab.reference_range == "Normal: 4.0–5.6"
        assert normalized_lab is lab  # Should modify in place
    
    def test_normalize_lab_result_no_max(self):
        """Test normalizing lab result with no maximum."""
        lab = LabResult("eGFR", 80, "mL/min/1.73m2", "2023-11-01")
        normalized_lab = BiomarkerNormalizer.normalize_lab_result(lab)
        
        assert "Normal: >60" in normalized_lab.reference_range
    
    def test_normalize_lab_result_no_min(self):
        """Test normalizing lab result with no minimum."""
        lab = LabResult("Total Cholesterol", 180, "mg/dL", "2023-11-01")
        normalized_lab = BiomarkerNormalizer.normalize_lab_result(lab)
        
        assert "Normal: <200" in normalized_lab.reference_range
    
    def test_normalize_unknown_lab_result(self):
        """Test normalizing unknown lab result."""
        lab = LabResult("Unknown Test", 100, "units", "2023-11-01")
        normalized_lab = BiomarkerNormalizer.normalize_lab_result(lab)
        
        assert normalized_lab.reference_range is None
    
    def test_get_status_indicator_normal(self):
        """Test status indicator for normal values."""
        lab = LabResult("HbA1c", 5.0, "%", "2023-11-01")
        status = BiomarkerNormalizer.get_status_indicator(lab)
        assert status == ""
    
    def test_get_status_indicator_high(self):
        """Test status indicator for high values."""
        lab = LabResult("HbA1c", 8.0, "%", "2023-11-01")
        status = BiomarkerNormalizer.get_status_indicator(lab)
        assert status == "↑"
    
    def test_get_status_indicator_low(self):
        """Test status indicator for low values."""
        lab = LabResult("HbA1c", 3.0, "%", "2023-11-01")
        status = BiomarkerNormalizer.get_status_indicator(lab)
        assert status == "↓"
    
    def test_get_status_indicator_unknown(self):
        """Test status indicator for unknown test."""
        lab = LabResult("Unknown Test", 100, "units", "2023-11-01")
        status = BiomarkerNormalizer.get_status_indicator(lab)
        assert status == ""
    
    def test_reference_ranges_completeness(self):
        """Test that reference ranges are defined for common tests."""
        common_tests = ["HbA1c", "Creatinine", "eGFR", "Fasting Glucose", "Total Cholesterol"]
        
        for test in common_tests:
            ref_range = BiomarkerNormalizer.get_reference_range(test)
            assert ref_range is not None, f"Reference range missing for {test}"
            assert ref_range.unit is not None, f"Unit missing for {test}"
