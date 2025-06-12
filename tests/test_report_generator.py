"""Tests for report generation in various formats."""
import pytest
import json
from src.report_generator import ReportGenerator
from src.models import PatientSummary, HealthSummary, LabResult, HealthDomain


class TestReportGenerator:
    """Test report generation functionality."""
    
    @pytest.fixture
    def sample_patient_summary(self):
        """Sample patient summary for testing."""
        renal_labs = [
            LabResult("Creatinine", 1.6, "mg/dL", "2023-11-01", 
                     reference_range="Normal: 0.6–1.3", health_domain=HealthDomain.RENAL),
            LabResult("eGFR", 54, "mL/min/1.73m2", "2023-11-01", 
                     reference_range="Normal: >60", health_domain=HealthDomain.RENAL)
        ]
        
        endocrine_labs = [
            LabResult("HbA1c", 7.2, "%", "2023-11-01", 
                     reference_range="Normal: 4.0–5.6", health_domain=HealthDomain.ENDOCRINE),
            LabResult("Fasting Glucose", 120, "mg/dL", "2023-11-01", 
                     reference_range="Normal: 70–99", health_domain=HealthDomain.ENDOCRINE)
        ]
        
        health_summaries = [
            HealthSummary(
                domain=HealthDomain.RENAL,
                lab_results=renal_labs,
                trends="Moderate kidney dysfunction – suggest nephrology consultation"
            ),
            HealthSummary(
                domain=HealthDomain.ENDOCRINE,
                lab_results=endocrine_labs,
                trends="Suboptimal diabetes control – suggest medication adjustment"
            )
        ]
        
        return PatientSummary(
            patient_id="PT123456",
            health_summaries=health_summaries,
            overall_summary="Patient has early CKD and diabetes requiring management."
        )
    
    def test_format_lab_result_line_with_reference(self):
        """Test formatting lab result line with reference range."""
        lab = LabResult("HbA1c", 7.2, "%", "2023-11-01", reference_range="Normal: 4.0–5.6")
        
        # Mock the status indicator
        from unittest.mock import patch
        with patch('src.report_generator.BiomarkerNormalizer.get_status_indicator', return_value="↑"):
            line = ReportGenerator.format_lab_result_line(lab, include_reference=True)
        
        assert "**HbA1c**:" in line
        assert "7.2 %" in line
        assert "↑" in line
        assert "(Normal: 4.0–5.6)" in line
    
    def test_format_lab_result_line_without_reference(self):
        """Test formatting lab result line without reference range."""
        lab = LabResult("HbA1c", 7.2, "%", "2023-11-01")
        
        from unittest.mock import patch
        with patch('src.report_generator.BiomarkerNormalizer.get_status_indicator', return_value=""):
            line = ReportGenerator.format_lab_result_line(lab, include_reference=False)
        
        assert "**HbA1c**:" in line
        assert "7.2 %" in line
        assert "Normal:" not in line
    
    def test_generate_markdown_report(self, sample_patient_summary):
        """Test generating markdown report."""
        report = ReportGenerator.generate_markdown_report(sample_patient_summary)
        
        assert "## Patient Summary – ID: PT123456" in report
        assert "**Health Domain: Renal**" in report
        assert "**Health Domain: Endocrine**" in report
        assert "**Creatinine**:" in report
        assert "**HbA1c**:" in report
        assert "🧠 **Summary**:" in report
        assert "early CKD and diabetes" in report
    
    def test_generate_latex_report(self, sample_patient_summary):
        """Test generating LaTeX report."""
        report = ReportGenerator.generate_latex_report(sample_patient_summary)
        
        assert "\\documentclass{article}" in report
        assert "\\section{Patient Summary - ID: PT123456}" in report
        assert "\\subsection{Renal}" in report
        assert "\\subsection{Endocrine}" in report
        assert "\\textbf{Creatinine}" in report
        assert "\\textbf{HbA1c}" in report
        assert "\\end{document}" in report
    
    def test_generate_json_report(self, sample_patient_summary):
        """Test generating JSON report."""
        report = ReportGenerator.generate_json_report(sample_patient_summary)
        
        assert isinstance(report, dict)
        assert report["patient_id"] == "PT123456"
        assert "health_summaries" in report
        assert len(report["health_summaries"]) == 2
        
        # Check that enums are converted to values
        for summary in report["health_summaries"]:
            assert isinstance(summary["domain"], str)
            assert summary["domain"] in ["Renal", "Endocrine"]
    
    def test_markdown_report_structure(self, sample_patient_summary):
        """Test markdown report has correct structure."""
        report = ReportGenerator.generate_markdown_report(sample_patient_summary)
        lines = report.split("\\n")
        
        # Check header
        assert any("## Patient Summary" in line for line in lines)
        
        # Check health domains
        assert any("**Health Domain: Renal**" in line for line in lines)
        assert any("**Health Domain: Endocrine**" in line for line in lines)
        
        # Check lab results (should be bullet points)
        lab_lines = [line for line in lines if line.startswith("- **")]
        assert len(lab_lines) >= 4  # At least 4 lab results
        
        # Check trends
        trend_lines = [line for line in lines if "**Trend**:" in line]
        assert len(trend_lines) >= 2  # At least 2 trend lines
        
        # Check overall summary
        assert any("🧠 **Summary**:" in line for line in lines)
    
    def test_latex_report_structure(self, sample_patient_summary):
        """Test LaTeX report has correct structure."""
        report = ReportGenerator.generate_latex_report(sample_patient_summary)
        
        # Check document structure
        assert "\\documentclass{article}" in report
        assert "\\begin{document}" in report
        assert "\\end{document}" in report
        
        # Check sections
        assert "\\section{Patient Summary" in report
        assert "\\subsection{Renal}" in report
        assert "\\subsection{Endocrine}" in report
        
        # Check itemize environments
        assert "\\begin{itemize}" in report
        assert "\\end{itemize}" in report
        
        # Check items
        assert "\\item \\textbf{" in report
    
    def test_empty_patient_summary(self):
        """Test generating reports with empty patient summary."""
        empty_summary = PatientSummary(
            patient_id="PT000000",
            health_summaries=[],
            overall_summary=None
        )
        
        markdown_report = ReportGenerator.generate_markdown_report(empty_summary)
        assert "PT000000" in markdown_report
        assert "## Patient Summary" in markdown_report
        
        latex_report = ReportGenerator.generate_latex_report(empty_summary)
        assert "PT000000" in latex_report
        assert "\\section{Patient Summary" in latex_report
        
        json_report = ReportGenerator.generate_json_report(empty_summary)
        assert json_report["patient_id"] == "PT000000"
        assert json_report["health_summaries"] == []
    
    def test_patient_summary_without_overall_summary(self):
        """Test generating reports without overall summary."""
        summary_without_overall = PatientSummary(
            patient_id="PT111111",
            health_summaries=[
                HealthSummary(
                    domain=HealthDomain.OTHER,
                    lab_results=[LabResult("Test", 100, "units", "2023-11-01")],
                    trends="Normal values"
                )
            ],
            overall_summary=None
        )
        
        markdown_report = ReportGenerator.generate_markdown_report(summary_without_overall)
        assert "PT111111" in markdown_report
        assert "🧠 **Summary**:" not in markdown_report
        
        latex_report = ReportGenerator.generate_latex_report(summary_without_overall)
        assert "PT111111" in latex_report
        assert "\\section{Summary}" not in latex_report
