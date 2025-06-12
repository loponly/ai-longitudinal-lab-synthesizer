"""Report generation in Markdown and LaTeX formats."""
from typing import Dict

from src.loinc_mapping import BiomarkerNormalizer
from src.models import PatientSummary


class ReportGenerator:
    """Generates clinical reports in various formats."""

    @staticmethod
    def format_lab_result_line(lab_result, include_reference: bool = True) -> str:
        """Format a single lab result line with status indicators."""
        from src.loinc_mapping import BiomarkerNormalizer

        status = BiomarkerNormalizer.get_status_indicator(lab_result)
        status_str = f" {status}" if status else ""

        if include_reference and lab_result.reference_range:
            ref_str = f" ({lab_result.reference_range})"
        else:
            ref_str = ""

        return f"- **{lab_result.test_name}**: {lab_result.value} {lab_result.unit}{status_str}{ref_str}"

    @staticmethod
    def generate_markdown_report(patient_summary: PatientSummary) -> str:
        """Generate a markdown report for patient summary."""
        report_lines = [
            f"## Patient Summary - ID: {patient_summary.patient_id}",
            ""
        ]

        # Group health summaries by domain
        for health_summary in patient_summary.health_summaries:
            domain_name = health_summary.domain.value
            report_lines.extend([
                f"**Health Domain: {domain_name}**"
            ])

            # Add lab results
            for lab_result in health_summary.lab_results:
                lab_line = ReportGenerator.format_lab_result_line(lab_result)
                report_lines.append(lab_line)

            # Add trends if available
            if health_summary.trends:
                report_lines.append(f"- **Trend**: {health_summary.trends}")

            report_lines.append("")  # Empty line between domains

        # Add overall summary if available
        if patient_summary.overall_summary:
            report_lines.extend([
                f"🧠 **Summary**: {patient_summary.overall_summary}"
            ])

        return "\\n".join(report_lines)

    @staticmethod
    def generate_latex_report(patient_summary: PatientSummary) -> str:
        """Generate a LaTeX report for patient summary."""
        latex_lines = [
            "\\documentclass{article}",
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage{amsmath}",
            "\\usepackage{booktabs}",
            "\\title{Patient Lab Summary}",
            "\\begin{document}",
            "\\maketitle",
            "",
            f"\\section{{Patient Summary - ID: {patient_summary.patient_id}}}",
            ""
        ]

        for health_summary in patient_summary.health_summaries:
            domain_name = health_summary.domain.value
            latex_lines.extend([
                f"\\subsection{{{domain_name}}}",
                "\\begin{itemize}"
            ])

            # Add lab results
            for lab_result in health_summary.lab_results:
                status = BiomarkerNormalizer.get_status_indicator(lab_result)
                status_str = f" {status}" if status else ""
                ref_str = f" ({lab_result.reference_range})" if lab_result.reference_range else ""

                latex_lines.append(
                    f"\\item \\textbf{{{lab_result.test_name}}}: "
                    f"{lab_result.value} {lab_result.unit}{status_str}{ref_str}"
                )

            # Add trends
            if health_summary.trends:
                latex_lines.append(f"\\item \\textbf{{Trend}}: {health_summary.trends}")

            latex_lines.extend([
                "\\end{itemize}",
                ""
            ])

        # Add overall summary
        if patient_summary.overall_summary:
            latex_lines.extend([
                "\\section{Summary}",
                patient_summary.overall_summary,
                ""
            ])

        latex_lines.append("\\end{document}")

        return "\\n".join(latex_lines)

    @staticmethod
    def generate_json_report(patient_summary: PatientSummary) -> Dict:
        """Generate a JSON-serializable report."""

        # Convert to dict but handle enums
        def convert_for_json(obj):
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    if hasattr(value, 'value'):  # Enum
                        result[key] = value.value
                    elif isinstance(value, list):
                        result[key] = [convert_for_json(item) for item in value]
                    elif hasattr(value, '__dict__'):
                        result[key] = convert_for_json(value)
                    else:
                        result[key] = value
                return result
            return obj

        return convert_for_json(patient_summary)
