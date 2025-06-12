"""Tests for health area classification."""
import pytest
from src.health_classifier import HealthAreaClassifier
from src.models import LabResult, HealthDomain


class TestHealthAreaClassifier:
    """Test health area classification functionality."""
    
    def test_classify_renal_tests(self):
        """Test classification of renal function tests."""
        creatinine = LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01")
        egfr = LabResult("eGFR", 54, "mL/min/1.73m2", "2023-11-01")
        bun = LabResult("BUN", 25, "mg/dL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(creatinine) == HealthDomain.RENAL
        assert HealthAreaClassifier.classify_lab_result(egfr) == HealthDomain.RENAL
        assert HealthAreaClassifier.classify_lab_result(bun) == HealthDomain.RENAL
    
    def test_classify_endocrine_tests(self):
        """Test classification of endocrine tests."""
        hba1c = LabResult("HbA1c", 7.2, "%", "2023-11-01")
        glucose = LabResult("Fasting Glucose", 120, "mg/dL", "2023-11-01")
        insulin = LabResult("Insulin", 15, "uU/mL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(hba1c) == HealthDomain.ENDOCRINE
        assert HealthAreaClassifier.classify_lab_result(glucose) == HealthDomain.ENDOCRINE
        assert HealthAreaClassifier.classify_lab_result(insulin) == HealthDomain.ENDOCRINE
    
    def test_classify_lipid_tests(self):
        """Test classification of lipid tests."""
        total_chol = LabResult("Total Cholesterol", 220, "mg/dL", "2023-11-01")
        hdl = LabResult("HDL Cholesterol", 35, "mg/dL", "2023-11-01")
        ldl = LabResult("LDL Cholesterol", 160, "mg/dL", "2023-11-01")
        triglycerides = LabResult("Triglycerides", 200, "mg/dL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(total_chol) == HealthDomain.LIPID
        assert HealthAreaClassifier.classify_lab_result(hdl) == HealthDomain.LIPID
        assert HealthAreaClassifier.classify_lab_result(ldl) == HealthDomain.LIPID
        assert HealthAreaClassifier.classify_lab_result(triglycerides) == HealthDomain.LIPID
    
    def test_classify_hematology_tests(self):
        """Test classification of hematology tests."""
        hemoglobin = LabResult("Hemoglobin", 10.5, "g/dL", "2023-11-01")
        hematocrit = LabResult("Hematocrit", 32, "%", "2023-11-01")
        wbc = LabResult("White Blood Cell Count", 12.5, "K/uL", "2023-11-01")
        platelets = LabResult("Platelet Count", 450, "K/uL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(hemoglobin) == HealthDomain.HEMATOLOGY
        assert HealthAreaClassifier.classify_lab_result(hematocrit) == HealthDomain.HEMATOLOGY
        assert HealthAreaClassifier.classify_lab_result(wbc) == HealthDomain.HEMATOLOGY
        assert HealthAreaClassifier.classify_lab_result(platelets) == HealthDomain.HEMATOLOGY
    
    def test_classify_liver_tests(self):
        """Test classification of liver function tests."""
        alt = LabResult("ALT", 65, "U/L", "2023-11-01")
        ast = LabResult("AST", 70, "U/L", "2023-11-01")
        bilirubin = LabResult("Total Bilirubin", 2.5, "mg/dL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(alt) == HealthDomain.LIVER
        assert HealthAreaClassifier.classify_lab_result(ast) == HealthDomain.LIVER
        assert HealthAreaClassifier.classify_lab_result(bilirubin) == HealthDomain.LIVER
    
    def test_classify_thyroid_tests(self):
        """Test classification of thyroid function tests."""
        tsh = LabResult("TSH", 8.5, "mIU/L", "2023-11-01")
        t4 = LabResult("Free T4", 0.8, "ng/dL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(tsh) == HealthDomain.THYROID
        assert HealthAreaClassifier.classify_lab_result(t4) == HealthDomain.THYROID
    
    def test_classify_case_insensitive(self):
        """Test case-insensitive classification."""
        creatinine_upper = LabResult("CREATININE", 1.6, "mg/dL", "2023-11-01")
        hba1c_lower = LabResult("hba1c", 7.2, "%", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(creatinine_upper) == HealthDomain.RENAL
        assert HealthAreaClassifier.classify_lab_result(hba1c_lower) == HealthDomain.ENDOCRINE
    
    def test_classify_partial_matching(self):
        """Test partial matching for test names."""
        random_glucose = LabResult("Random Glucose Test", 180, "mg/dL", "2023-11-01")
        serum_creatinine = LabResult("Serum Creatinine Level", 1.8, "mg/dL", "2023-11-01")
        
        assert HealthAreaClassifier.classify_lab_result(random_glucose) == HealthDomain.ENDOCRINE
        assert HealthAreaClassifier.classify_lab_result(serum_creatinine) == HealthDomain.RENAL
    
    def test_classify_unknown_test(self):
        """Test classification of unknown test."""
        unknown = LabResult("Some Unknown Test", 100, "units", "2023-11-01")
        assert HealthAreaClassifier.classify_lab_result(unknown) == HealthDomain.OTHER
    
    def test_classify_all_labs(self):
        """Test classifying multiple lab results."""
        labs = [
            LabResult("HbA1c", 7.2, "%", "2023-11-01"),
            LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01"),
            LabResult("Total Cholesterol", 220, "mg/dL", "2023-11-01")
        ]
        
        classified_labs = HealthAreaClassifier.classify_all_labs(labs)
        
        assert classified_labs[0].health_domain == HealthDomain.ENDOCRINE
        assert classified_labs[1].health_domain == HealthDomain.RENAL
        assert classified_labs[2].health_domain == HealthDomain.LIPID
        assert classified_labs is labs  # Should modify in place
    
    def test_group_by_domain(self):
        """Test grouping lab results by health domain."""
        labs = [
            LabResult("HbA1c", 7.2, "%", "2023-11-01"),
            LabResult("Fasting Glucose", 120, "mg/dL", "2023-11-01"),
            LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01"),
            LabResult("eGFR", 54, "mL/min/1.73m2", "2023-11-01"),
            LabResult("Total Cholesterol", 220, "mg/dL", "2023-11-01")
        ]
        
        groups = HealthAreaClassifier.group_by_domain(labs)
        
        assert HealthDomain.ENDOCRINE in groups
        assert HealthDomain.RENAL in groups
        assert HealthDomain.LIPID in groups
        
        assert len(groups[HealthDomain.ENDOCRINE]) == 2
        assert len(groups[HealthDomain.RENAL]) == 2
        assert len(groups[HealthDomain.LIPID]) == 1
        
        # Check that all labs have health_domain set
        for lab in labs:
            assert lab.health_domain is not None
    
    def test_group_by_domain_empty_list(self):
        """Test grouping empty lab results list."""
        groups = HealthAreaClassifier.group_by_domain([])
        assert groups == {}
