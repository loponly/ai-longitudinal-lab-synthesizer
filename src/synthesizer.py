"""Main synthesizer that orchestrates the lab data processing pipeline."""
import json
from typing import Any, Dict, List

from src.health_classifier import HealthAreaClassifier
from src.loinc_mapping import BiomarkerNormalizer, LOINCMapper
from src.models import HealthDomain, HealthSummary, PatientData, PatientSummary
from src.report_generator import ReportGenerator
from src.trend_analyzer import TrendAnalyzer


class LabDataSynthesizer:
    """Main orchestrator for lab data synthesis and report generation."""

    def __init__(self):
        """Initialize the synthesizer."""
        pass

    def process_patient_data(self, patient_data: PatientData) -> PatientSummary:
        """Process patient lab data through the complete pipeline."""
        # Step 1: Map LOINC codes
        for lab_result in patient_data.labs:
            LOINCMapper.map_lab_result(lab_result)

        # Step 2: Normalize biomarkers and add reference ranges
        for lab_result in patient_data.labs:
            BiomarkerNormalizer.normalize_lab_result(lab_result)

        # Step 3: Classify into health areas
        HealthAreaClassifier.classify_all_labs(patient_data.labs)

        # Step 4: Group by health domain
        domain_groups = HealthAreaClassifier.group_by_domain(patient_data.labs)

        # Step 5: Generate health summaries with trends
        health_summaries = []
        for domain, labs in domain_groups.items():
            if domain != HealthDomain.OTHER or labs:  # Include OTHER only if has labs
                health_summary = TrendAnalyzer.generate_health_summary(domain, labs)
                health_summaries.append(health_summary)

        # Step 6: Generate overall summary
        overall_summary = self._generate_overall_summary(health_summaries)

        return PatientSummary(
            patient_id=patient_data.patient_id,
            health_summaries=health_summaries,
            overall_summary=overall_summary
        )

    def _generate_overall_summary(self, health_summaries: List[HealthSummary]) -> str:
        """Generate an overall clinical summary."""
        issues = []
        recommendations = []

        for summary in health_summaries:
            if summary.trends and summary.trends != "Values within normal limits":

                # Extract key issues
                if "elevated" in summary.trends.lower() or "↑" in summary.trends:
                    if summary.domain == HealthDomain.RENAL:
                        issues.append("early CKD")
                    elif summary.domain == HealthDomain.ENDOCRINE:
                        issues.append("pre-diabetes")
                    elif summary.domain == HealthDomain.LIPID:
                        issues.append("dyslipidemia")

                # Extract recommendations
                if "nephrology referral" in summary.trends:
                    recommendations.append("nephrology referral")
                if "follow-up" in summary.trends.lower():
                    recommendations.append("follow-up testing")
                if "lifestyle" in summary.trends.lower():
                    recommendations.append("lifestyle modifications")

        if issues:
            summary_text = f"Patient trending toward {' and '.join(issues)}."
            if recommendations:
                summary_text += f" Recommend {' and '.join(set(recommendations))}."
            return summary_text

        return "Overall stable lab values with no significant abnormalities."

    def synthesize_from_json(self, json_data: str) -> str:
        """Process JSON input and return markdown report."""
        # Parse JSON input
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        # Create patient data object
        patient_data = PatientData(**data)

        # Process through pipeline
        patient_summary = self.process_patient_data(patient_data)

        # Generate markdown report
        return ReportGenerator.generate_markdown_report(patient_summary)

    def synthesize_to_formats(self, json_data: str) -> Dict[str, Any]:
        """Process input and return reports in multiple formats."""
        # Parse JSON input
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        # Create patient data object
        patient_data = PatientData(**data)

        # Process through pipeline
        patient_summary = self.process_patient_data(patient_data)

        return {
            "markdown": ReportGenerator.generate_markdown_report(patient_summary),
            "latex": ReportGenerator.generate_latex_report(patient_summary),
            "json": ReportGenerator.generate_json_report(patient_summary),
            "patient_summary": patient_summary
        }
