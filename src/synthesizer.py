"""Main synthesizer that orchestrates the lab data processing pipeline."""
import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from langroid import ChatAgent, ChatAgentConfig, Task
from langroid.language_models import MockLMConfig, OpenAIGPTConfig

from src.health_classifier import HealthAreaClassifier
from src.loinc_mapping import BiomarkerNormalizer, LOINCMapper
from src.models import HealthDomain, HealthSummary, PatientData, PatientSummary
from src.report_generator import ReportGenerator
from src.trend_analyzer import TrendAnalyzer


class LabDataSynthesizer:
    """Main orchestrator for lab data synthesis and report generation."""

    def __init__(self, use_mock=False):
        """Initialize the synthesizer with Langroid agents."""
        load_dotenv()
        # Check if OpenAI API key is available, otherwise use mock
        if use_mock or not os.getenv("OPENAI_API_KEY"):
            print("🤖 Using mock responses for demonstration")
            self.llm_config = MockLMConfig()
        else:
            self.llm_config = OpenAIGPTConfig(
                chat_model="gpt-4o-mini",
                chat_context_length=16000,
            )

        # Initialize specialized agents
        self._setup_agents()

    def _setup_agents(self):
        """Set up specialized Langroid agents for different analysis tasks."""
        # Lab Classification Agent
        self.classifier_agent = ChatAgent(
            ChatAgentConfig(
                name="LabClassifier",
                llm=self.llm_config,
                system_message="""
                You are a medical lab classification expert. Your role is to:
                1. Analyze lab test results and classify them into health domains
                2. Identify abnormal values based on reference ranges
                3. Determine clinical significance of results

                Health domains include: RENAL, ENDOCRINE, LIPID, 
                HEPATIC, HEMATOLOGIC, CARDIAC, OTHER

                For each lab result, provide:
                - Health domain classification
                - Normal/abnormal status with direction (↑/↓)
                - Clinical interpretation
                """,
            )
        )

        # Trend Analysis Agent
        self.trend_agent = ChatAgent(
            ChatAgentConfig(
                name="TrendAnalyzer",
                llm=self.llm_config,
                system_message="""
                You are a medical trend analysis expert. Your role is to:
                1. Analyze longitudinal lab data for trends
                2. Identify patterns and progressions
                3. Assess clinical implications of trends
                4. Suggest appropriate follow-up actions

                Provide concise trend analysis with:
                - Direction and magnitude of changes
                - Clinical significance
                - Recommendations for monitoring or intervention
                """,
            )
        )

        # Report Generation Agent
        self.report_agent = ChatAgent(
            ChatAgentConfig(
                name="ReportGenerator",
                llm=self.llm_config,
                system_message="""
                You are a medical report generation expert. Your role is to:
                1. Synthesize lab analysis into comprehensive reports
                2. Create clear, structured clinical summaries
                3. Provide actionable recommendations

                Generate reports in markdown format with:
                - Patient summary header
                - Health domain sections
                - Trend analysis
                - Overall clinical summary with recommendations
                """,
            )
        )

    def process_patient_data(self, patient_data: PatientData) -> PatientSummary:
        """Process patient lab data through the Langroid agent pipeline."""
        # Step 1: Traditional mapping and normalization (keeping existing logic)
        for lab_result in patient_data.labs:
            LOINCMapper.map_lab_result(lab_result)
            BiomarkerNormalizer.normalize_lab_result(lab_result)

        # Step 2: Traditional classification (always performed for reliability)
        HealthAreaClassifier.classify_all_labs(patient_data.labs)
        domain_groups = HealthAreaClassifier.group_by_domain(patient_data.labs)

        # Step 3: Enhanced analysis with agents (if not using mock)
        health_summaries = []
        for domain, labs in domain_groups.items():
            if domain != HealthDomain.OTHER or labs:
                if isinstance(self.llm_config, MockLMConfig):
                    # Use traditional trend analysis for testing
                    health_summary = TrendAnalyzer.generate_health_summary(domain, labs)
                else:
                    # Use agent for enhanced trend analysis
                    try:
                        trend_data = self._format_domain_data_for_trend_analysis(
                            domain, labs)

                        trend_task = Task(
                            self.trend_agent,
                            name=f"analyze_trends_{domain.value}",
                            system_message=(
                                f"Analyze trends for {domain.value} domain "
                                "lab results:"),
                        )

                        trend_result = trend_task.run(trend_data)

                        # Create health summary with agent-enhanced analysis
                        health_summary = self._create_enhanced_health_summary(
                            domain, labs, trend_result.content)
                    except Exception as e:
                        print(f"Agent analysis failed, falling back to traditional "
                              f"analysis: {e}")
                        health_summary = TrendAnalyzer.generate_health_summary(
                            domain, labs)

                health_summaries.append(health_summary)

        # Step 4: Generate overall summary
        if isinstance(self.llm_config, MockLMConfig):
            # Use traditional summary generation for testing
            overall_summary = self._generate_overall_summary(health_summaries)
        else:
            # Use agent for enhanced summary generation
            try:
                overall_summary = self._generate_overall_summary_with_agent(
                    health_summaries, patient_data)
            except Exception as e:
                print(f"Agent summary failed, falling back to traditional "
                      f"summary: {e}")
                overall_summary = self._generate_overall_summary(health_summaries)

        return PatientSummary(
            patient_id=patient_data.patient_id,
            health_summaries=health_summaries,
            overall_summary=overall_summary
        )

    def _format_lab_data_for_agent(self, labs) -> str:
        """Format lab data for Langroid agent processing."""
        lab_strings = []
        for lab in labs:
            lab_str = f"- {lab.test_name}: {lab.value} {lab.unit}"
            if hasattr(lab, 'reference_range') and lab.reference_range:
                lab_str += f" (Normal: {lab.reference_range})"
            if hasattr(lab, 'date'):
                lab_str += f" [{lab.date}]"
            lab_strings.append(lab_str)

        return "\n".join(lab_strings)

    def _format_domain_data_for_trend_analysis(self, domain: HealthDomain, labs) -> str:
        """Format domain-specific lab data for trend analysis."""
        domain_str = f"Health Domain: {domain.value}\n"
        domain_str += self._format_lab_data_for_agent(labs)
        return domain_str

    def _create_enhanced_health_summary(self, domain: HealthDomain, labs, 
                                       agent_analysis: str) -> HealthSummary:
        """Create health summary enhanced with agent analysis."""
        # Use traditional method as base
        base_summary = TrendAnalyzer.generate_health_summary(domain, labs)

        # Enhance with agent analysis
        base_summary.trends = agent_analysis.strip()

        return base_summary

    def _generate_overall_summary_with_agent(
            self, health_summaries: List[HealthSummary], 
            patient_data: PatientData) -> str:
        """Generate overall summary using Langroid agent."""
        summary_data = f"Patient ID: {patient_data.patient_id}\n\n"

        for summary in health_summaries:
            summary_data += f"**{summary.domain.value} Domain:**\n"
            for lab in summary.labs:
                summary_data += f"- {lab.test_name}: {lab.value} {lab.unit}"
                if hasattr(lab, 'status'):
                    summary_data += f" ({lab.status})"
                summary_data += "\n"

            if summary.trends:
                summary_data += f"Trends: {summary.trends}\n"
            summary_data += "\n"

        summary_task = Task(
            self.report_agent,
            name="generate_overall_summary",
            system_message=(
                "Generate a concise overall clinical summary with key "
                "findings and recommendations:"),
        )

        result = summary_task.run(summary_data)
        return result.content.strip()

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

        # Process through Langroid-enhanced pipeline
        patient_summary = self.process_patient_data(patient_data)

        # Generate markdown report
        if isinstance(self.llm_config, MockLMConfig):
            # Use traditional markdown generation for testing
            markdown_report = ReportGenerator.generate_markdown_report(patient_summary)
        else:
            # Generate enhanced markdown report using Langroid agent
            try:
                markdown_report = self._generate_enhanced_markdown_report(patient_summary)
            except Exception as e:
                print(f"Agent markdown generation failed, falling back to traditional: {e}")
                markdown_report = ReportGenerator.generate_markdown_report(patient_summary)

        return {
            "markdown": markdown_report,
            "latex": ReportGenerator.generate_latex_report(patient_summary),
            "json": ReportGenerator.generate_json_report(patient_summary),
            "patient_summary": patient_summary
        }

    def _generate_enhanced_markdown_report(self, patient_summary: PatientSummary) -> str:
        """Generate markdown report using Langroid agent for enhanced formatting."""
        # Prepare comprehensive data for the report agent
        report_data = f"Patient ID: {patient_summary.patient_id}\n\n"

        for summary in patient_summary.health_summaries:
            report_data += f"**{summary.domain.value} Domain:**\n"
            for lab in summary.labs:
                report_data += f"- {lab.test_name}: {lab.value} {lab.unit}"
                if hasattr(lab, 'reference_range') and lab.reference_range:
                    report_data += f" (Normal: {lab.reference_range})"
                if hasattr(lab, 'status') and lab.status:
                    report_data += f" {lab.status}"
                report_data += "\n"

            if summary.trends:
                report_data += f"Analysis: {summary.trends}\n"
            report_data += "\n"

        if patient_summary.overall_summary:
            report_data += f"Overall Summary: {patient_summary.overall_summary}\n"

        # Use Langroid agent to generate the final report
        report_task = Task(
            self.report_agent,
            name="generate_markdown_report",
            system_message="""Generate a comprehensive medical lab report in markdown format. 
            Structure it with:
            1. Patient Summary header
            2. Health domain sections with lab values, reference ranges, and status indicators (↑/↓)
            3. Trend analysis for each domain
            4. Overall clinical summary with 🧠 emoji
            
            Use proper markdown formatting with headers, bold text, and clear organization.""",
        )

        result = report_task.run(report_data)
        return result.content.strip()
