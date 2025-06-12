"""Tests for trend analysis and clinical recommendations."""
import pytest
from src.trend_analyzer import TrendAnalyzer
from src.models import LabResult, HealthDomain, HealthSummary


class TestTrendAnalyzer:
    """Test trend analysis functionality."""
    
    def test_analyze_renal_function_normal(self):
        """Test renal function analysis with normal values."""
        labs = [
            LabResult("Creatinine", 1.0, "mg/dL", "2023-11-01"),
            LabResult("eGFR", 85, "mL/min/1.73m2", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_renal_function(labs)
        assert "Stable renal function" in trend
    
    def test_analyze_renal_function_mild_impairment(self):
        """Test renal function analysis with mild impairment."""
        labs = [
            LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01"),
            LabResult("eGFR", 54, "mL/min/1.73m2", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_renal_function(labs)
        assert "elevated creatinine" in trend.lower()
        assert "kidney dysfunction" in trend.lower()
        assert "monitor renal function" in trend.lower()
    
    def test_analyze_renal_function_severe_impairment(self):
        """Test renal function analysis with severe impairment."""
        labs = [
            LabResult("Creatinine", 2.8, "mg/dL", "2023-11-01"),
            LabResult("eGFR", 25, "mL/min/1.73m2", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_renal_function(labs)
        assert "nephrology referral" in trend.lower()
        assert ("severe" in trend.lower() or "stage 4" in trend.lower())
    
    def test_analyze_diabetes_control_normal(self):
        """Test diabetes control analysis with normal values."""
        labs = [
            LabResult("HbA1c", 5.2, "%", "2023-11-01"),
            LabResult("Fasting Glucose", 90, "mg/dL", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_diabetes_control(labs)
        assert "Good glucose control" in trend
    
    def test_analyze_diabetes_control_prediabetic(self):
        """Test diabetes control analysis with prediabetic values."""
        labs = [
            LabResult("HbA1c", 6.0, "%", "2023-11-01"),
            LabResult("Fasting Glucose", 105, "mg/dL", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_diabetes_control(labs)
        assert ("pre-diabetic" in trend.lower() or "impaired" in trend.lower())
        assert "lifestyle modifications" in trend.lower()
    
    def test_analyze_diabetes_control_diabetic(self):
        """Test diabetes control analysis with diabetic values."""
        labs = [
            LabResult("HbA1c", 9.5, "%", "2023-11-01"),
            LabResult("Fasting Glucose", 180, "mg/dL", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_diabetes_control(labs)
        assert ("poor" in trend.lower() or "diabetic" in trend.lower())
        assert ("intensify" in trend.lower() or "management" in trend.lower())
    
    def test_analyze_lipid_profile_normal(self):
        """Test lipid profile analysis with normal values."""
        labs = [
            LabResult("Total Cholesterol", 180, "mg/dL", "2023-11-01"),
            LabResult("HDL Cholesterol", 50, "mg/dL", "2023-11-01"),
            LabResult("LDL Cholesterol", 90, "mg/dL", "2023-11-01"),
            LabResult("Triglycerides", 120, "mg/dL", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_lipid_profile(labs)
        assert "Acceptable lipid profile" in trend
    
    def test_analyze_lipid_profile_abnormal(self):
        """Test lipid profile analysis with abnormal values."""
        labs = [
            LabResult("Total Cholesterol", 250, "mg/dL", "2023-11-01"),
            LabResult("HDL Cholesterol", 30, "mg/dL", "2023-11-01"),
            LabResult("LDL Cholesterol", 160, "mg/dL", "2023-11-01"),
            LabResult("Triglycerides", 200, "mg/dL", "2023-11-01")
        ]
        
        trend = TrendAnalyzer.analyze_lipid_profile(labs)
        assert "elevated" in trend.lower()
        assert ("statin" in trend.lower() or "lipid management" in trend.lower())
    
    def test_generate_health_summary_renal(self):
        """Test generating health summary for renal domain."""
        labs = [
            LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01"),
            LabResult("eGFR", 54, "mL/min/1.73m2", "2023-11-01")
        ]
        
        summary = TrendAnalyzer.generate_health_summary(HealthDomain.RENAL, labs)
        
        assert summary.domain == HealthDomain.RENAL
        assert summary.lab_results == labs
        assert summary.trends is not None
        assert len(summary.trends) > 0
    
    def test_generate_health_summary_endocrine(self):
        """Test generating health summary for endocrine domain."""
        labs = [
            LabResult("HbA1c", 7.2, "%", "2023-11-01"),
            LabResult("Fasting Glucose", 140, "mg/dL", "2023-11-01")
        ]
        
        summary = TrendAnalyzer.generate_health_summary(HealthDomain.ENDOCRINE, labs)
        
        assert summary.domain == HealthDomain.ENDOCRINE
        assert summary.lab_results == labs
        assert summary.trends is not None
        assert len(summary.trends) > 0
    
    def test_generate_health_summary_lipid(self):
        """Test generating health summary for lipid domain."""
        labs = [
            LabResult("Total Cholesterol", 250, "mg/dL", "2023-11-01"),
            LabResult("LDL Cholesterol", 160, "mg/dL", "2023-11-01")
        ]
        
        summary = TrendAnalyzer.generate_health_summary(HealthDomain.LIPID, labs)
        
        assert summary.domain == HealthDomain.LIPID
        assert summary.lab_results == labs
        assert summary.trends is not None
        assert len(summary.trends) > 0
    
    def test_generate_health_summary_other_domain(self):
        """Test generating health summary for other/unknown domain."""
        labs = [
            LabResult("Custom Test", 100, "units", "2023-11-01")
        ]
        
        summary = TrendAnalyzer.generate_health_summary(HealthDomain.OTHER, labs)
        
        assert summary.domain == HealthDomain.OTHER
        assert summary.lab_results == labs
        assert summary.trends is not None
        # Should provide generic analysis
        assert ("normal limits" in summary.trends.lower() or 
                "follow up" in summary.trends.lower())
    
    def test_generate_health_summary_empty_labs(self):
        """Test generating health summary with empty lab list."""
        summary = TrendAnalyzer.generate_health_summary(HealthDomain.RENAL, [])
        
        assert summary.domain == HealthDomain.RENAL
        assert summary.lab_results == []
        assert summary.trends is not None
