"""Clinical trend analysis and recommendations."""
from typing import List

from src.models import HealthDomain, HealthSummary, LabResult

# Clinical thresholds as constants
CREATININE_NORMAL_UPPER = 1.3  # mg/dL
CREATININE_HIGH_THRESHOLD = 2.0  # mg/dL
EGFR_NORMAL_LOWER = 60  # mL/min/1.73m2
EGFR_STAGE_4_THRESHOLD = 30  # mL/min/1.73m2
EGFR_STAGE_3B_THRESHOLD = 45  # mL/min/1.73m2
EGFR_MILD_DECREASE_THRESHOLD = 90  # mL/min/1.73m2

HBA1C_DIABETES_THRESHOLD = 6.5  # %
HBA1C_POOR_CONTROL_THRESHOLD = 9.0  # %
HBA1C_SUBOPTIMAL_THRESHOLD = 7.0  # %
HBA1C_PREDIABETES_THRESHOLD = 5.7  # %

GLUCOSE_DIABETES_THRESHOLD = 126  # mg/dL
GLUCOSE_IMPAIRED_THRESHOLD = 100  # mg/dL

CHOLESTEROL_HIGH_THRESHOLD = 200  # mg/dL
LDL_HIGH_THRESHOLD = 100  # mg/dL
HDL_LOW_THRESHOLD = 40  # mg/dL
TRIGLYCERIDES_HIGH_THRESHOLD = 150  # mg/dL


class TrendAnalyzer:
    """Analyzes lab trends and generates clinical recommendations."""

    @staticmethod
    def analyze_renal_function(labs: List[LabResult]) -> str:
        """Analyze renal function trends and recommendations."""
        creatinine_labs = [lab for lab in labs if "creatinine" in lab.test_name.lower()]
        egfr_labs = [lab for lab in labs if "gfr" in lab.test_name.lower()]

        trends = []
        recommendations = []

        # Analyze creatinine
        for lab in creatinine_labs:
            if lab.value > CREATININE_NORMAL_UPPER:  # Above normal
                if lab.value > CREATININE_HIGH_THRESHOLD:
                    trends.append("Significantly elevated creatinine")
                    recommendations.append("urgent nephrology referral")
                else:
                    trends.append("Mildly elevated creatinine")
                    recommendations.append("monitor renal function")

        # Analyze eGFR
        for lab in egfr_labs:
            if lab.value < EGFR_NORMAL_LOWER:
                if lab.value < EGFR_STAGE_4_THRESHOLD:
                    trends.append("Severe kidney dysfunction (Stage 4 CKD)")
                    recommendations.append("nephrology referral and CKD management")
                elif lab.value < EGFR_STAGE_3B_THRESHOLD:
                    trends.append("Moderate-severe kidney dysfunction (Stage 3b CKD)")
                    recommendations.append("nephrology referral")
                else:
                    trends.append("Moderate kidney dysfunction (Stage 3a CKD)")
                    recommendations.append("monitor renal function")
            elif lab.value < EGFR_MILD_DECREASE_THRESHOLD:
                # Only flag as mild decrease if creatinine is also elevated
                if any(c.value > CREATININE_NORMAL_UPPER for c in creatinine_labs):
                    trends.append("Mild decrease in kidney function")

        if trends:
            trend_text = "; ".join(trends)
            if recommendations:
                trend_text += f" - suggest {', '.join(recommendations)}"
            return trend_text

        return "Stable renal function"

    @staticmethod
    def analyze_diabetes_control(labs: List[LabResult]) -> str:
        """Analyze diabetes control and glucose trends."""
        hba1c_labs = [lab for lab in labs if "a1c" in lab.test_name.lower()]
        glucose_labs = [lab for lab in labs if "glucose" in lab.test_name.lower()]

        trends = []
        recommendations = []

        # Analyze HbA1c and glucose levels
        trends.extend(TrendAnalyzer._analyze_hba1c_levels(hba1c_labs, recommendations))
        trends.extend(TrendAnalyzer._analyze_glucose_levels(glucose_labs, recommendations))

        if trends:
            trend_text = "; ".join(trends)
            if recommendations:
                trend_text += f" - suggest {', '.join(recommendations)}"
            return trend_text

        return "Good glucose control"

    @staticmethod
    def _analyze_hba1c_levels(hba1c_labs: List[LabResult], recommendations: List[str]) -> List[str]:
        """Analyze HbA1c levels and add recommendations."""
        trends = []
        for lab in hba1c_labs:
            if lab.value >= HBA1C_DIABETES_THRESHOLD:
                if lab.value >= HBA1C_POOR_CONTROL_THRESHOLD:
                    trends.append("Poor diabetes control")
                    recommendations.append("intensify diabetes management")
                elif lab.value >= HBA1C_SUBOPTIMAL_THRESHOLD:
                    trends.append("Suboptimal diabetes control")
                    recommendations.append("optimize diabetes therapy")
                else:
                    trends.append("Borderline diabetes control")
            elif lab.value >= HBA1C_PREDIABETES_THRESHOLD:
                trends.append("Pre-diabetic range")
                recommendations.append("lifestyle modifications and monitoring")
        return trends

    @staticmethod
    def _analyze_glucose_levels(glucose_labs: List[LabResult], recommendations: List[str]) -> List[str]:
        """Analyze glucose levels and add recommendations."""
        trends = []
        for lab in glucose_labs:
            if "fasting" in lab.test_name.lower():
                if lab.value >= GLUCOSE_DIABETES_THRESHOLD:
                    trends.append("Diabetic fasting glucose")
                elif lab.value >= GLUCOSE_IMPAIRED_THRESHOLD:
                    trends.append("Impaired fasting glucose")
        return trends

    @staticmethod
    def analyze_lipid_profile(labs: List[LabResult]) -> str:
        """Analyze lipid profile and cardiovascular risk."""
        cholesterol_labs = [lab for lab in labs if "cholesterol" in lab.test_name.lower()]
        triglyceride_labs = [lab for lab in labs if "triglyceride" in lab.test_name.lower()]

        trends = []
        recommendations = []

        for lab in cholesterol_labs:
            if "total" in lab.test_name.lower() and lab.value > CHOLESTEROL_HIGH_THRESHOLD:
                trends.append("Elevated total cholesterol")
                recommendations.append("lipid management")
            elif "ldl" in lab.test_name.lower() and lab.value > LDL_HIGH_THRESHOLD:
                trends.append("Elevated LDL cholesterol")
                recommendations.append("statin therapy consideration")
            elif "hdl" in lab.test_name.lower() and lab.value < HDL_LOW_THRESHOLD:
                trends.append("Low HDL cholesterol")
                recommendations.append("lifestyle modifications")

        for lab in triglyceride_labs:
            if lab.value > TRIGLYCERIDES_HIGH_THRESHOLD:
                trends.append("Elevated triglycerides")
                recommendations.append("dietary modifications")

        if trends:
            trend_text = "; ".join(trends)
            if recommendations:
                trend_text += f" - suggest {', '.join(recommendations)}"
            return trend_text

        return "Acceptable lipid profile"

    @classmethod
    def generate_health_summary(cls, domain: HealthDomain, labs: List[LabResult]) -> HealthSummary:
        """Generate a health summary for a specific domain."""
        trends = ""

        if domain == HealthDomain.RENAL:
            trends = cls.analyze_renal_function(labs)
        elif domain == HealthDomain.ENDOCRINE:
            trends = cls.analyze_diabetes_control(labs)
        elif domain == HealthDomain.LIPID:
            trends = cls.analyze_lipid_profile(labs)
        else:
            # Generic analysis for other domains
            abnormal_labs = []
            for lab in labs:
                from src.loinc_mapping import BiomarkerNormalizer
                status = BiomarkerNormalizer.get_status_indicator(lab)
                if status:
                    abnormal_labs.append(f"{lab.test_name} {status}")

            if abnormal_labs:
                trends = f"Abnormal values: {', '.join(abnormal_labs)} - follow up as clinically indicated"
            else:
                trends = "Values within normal limits"

        return HealthSummary(
            domain=domain,
            lab_results=labs,
            trends=trends
        )
