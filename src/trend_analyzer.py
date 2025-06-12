"""Clinical trend analysis and recommendations."""
from typing import List, Optional, Dict
from src.models import LabResult, HealthDomain, HealthSummary


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
            if lab.value > 1.3:  # Above normal
                if lab.value > 2.0:
                    trends.append("Significantly elevated creatinine")
                    recommendations.append("urgent nephrology referral")
                else:
                    trends.append("Mildly elevated creatinine")
                    recommendations.append("monitor renal function")
        
        # Analyze eGFR
        for lab in egfr_labs:
            if lab.value < 60:
                if lab.value < 30:
                    trends.append("Severe kidney dysfunction (Stage 4 CKD)")
                    recommendations.append("nephrology referral and CKD management")
                elif lab.value < 45:
                    trends.append("Moderate-severe kidney dysfunction (Stage 3b CKD)")
                    recommendations.append("nephrology referral")
                else:
                    trends.append("Moderate kidney dysfunction (Stage 3a CKD)")
                    recommendations.append("monitor renal function")
            elif lab.value < 90:
                trends.append("Mild decrease in kidney function")
        
        if trends:
            trend_text = "; ".join(trends)
            if recommendations:
                trend_text += f" – suggest {', '.join(recommendations)}"
            return trend_text
        
        return "Stable renal function"
    
    @staticmethod
    def analyze_diabetes_control(labs: List[LabResult]) -> str:
        """Analyze diabetes control and glucose trends."""
        hba1c_labs = [lab for lab in labs if "a1c" in lab.test_name.lower()]
        glucose_labs = [lab for lab in labs if "glucose" in lab.test_name.lower()]
        
        trends = []
        recommendations = []
        
        # Analyze HbA1c
        for lab in hba1c_labs:
            if lab.value >= 6.5:
                if lab.value >= 9.0:
                    trends.append("Poor diabetes control")
                    recommendations.append("intensify diabetes management")
                elif lab.value >= 7.0:
                    trends.append("Suboptimal diabetes control")
                    recommendations.append("optimize diabetes therapy")
                else:
                    trends.append("Borderline diabetes control")
            elif lab.value >= 5.7:
                trends.append("Pre-diabetic range")
                recommendations.append("lifestyle modifications and monitoring")
        
        # Analyze glucose
        for lab in glucose_labs:
            if "fasting" in lab.test_name.lower():
                if lab.value >= 126:
                    trends.append("Diabetic fasting glucose")
                elif lab.value >= 100:
                    trends.append("Impaired fasting glucose")
        
        if trends:
            trend_text = "; ".join(trends)
            if recommendations:
                trend_text += f" – suggest {', '.join(recommendations)}"
            return trend_text
        
        return "Good glucose control"
    
    @staticmethod
    def analyze_lipid_profile(labs: List[LabResult]) -> str:
        """Analyze lipid profile and cardiovascular risk."""
        cholesterol_labs = [lab for lab in labs if "cholesterol" in lab.test_name.lower()]
        triglyceride_labs = [lab for lab in labs if "triglyceride" in lab.test_name.lower()]
        
        trends = []
        recommendations = []
        
        for lab in cholesterol_labs:
            if "total" in lab.test_name.lower() and lab.value > 200:
                trends.append("Elevated total cholesterol")
                recommendations.append("lipid management")
            elif "ldl" in lab.test_name.lower() and lab.value > 100:
                trends.append("Elevated LDL cholesterol")
                recommendations.append("statin therapy consideration")
            elif "hdl" in lab.test_name.lower() and lab.value < 40:
                trends.append("Low HDL cholesterol")
                recommendations.append("lifestyle modifications")
        
        for lab in triglyceride_labs:
            if lab.value > 150:
                trends.append("Elevated triglycerides")
                recommendations.append("dietary modifications")
        
        if trends:
            trend_text = "; ".join(trends)
            if recommendations:
                trend_text += f" – suggest {', '.join(recommendations)}"
            return trend_text
        
        return "Acceptable lipid profile"
    
    @classmethod
    def generate_health_summary(cls, domain: HealthDomain, labs: List[LabResult]) -> HealthSummary:
        """Generate a health summary for a specific domain."""
        trends = ""
        recommendations = ""
        
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
                trends = f"Abnormal values: {', '.join(abnormal_labs)} – follow up as clinically indicated"
            else:
                trends = "Values within normal limits"
        
        return HealthSummary(
            domain=domain,
            lab_results=labs,
            trends=trends
        )
