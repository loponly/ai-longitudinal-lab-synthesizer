"""Health area classification using rules and patterns."""
from typing import ClassVar, Dict, List

from src.models import HealthDomain, LabResult


class HealthAreaClassifier:
    """Classifies lab results into health domains using rule-based logic."""

    # Mapping of test names to health domains
    TEST_DOMAIN_MAP: ClassVar[Dict[str, HealthDomain]] = {
        # Renal/Kidney
        "Creatinine": HealthDomain.RENAL,
        "Serum Creatinine": HealthDomain.RENAL,
        "eGFR": HealthDomain.RENAL,
        "Estimated GFR": HealthDomain.RENAL,
        "BUN": HealthDomain.RENAL,
        "Blood Urea Nitrogen": HealthDomain.RENAL,
        "Albumin": HealthDomain.RENAL,
        "Protein": HealthDomain.RENAL,

        # Endocrine/Diabetes
        "HbA1c": HealthDomain.ENDOCRINE,
        "Hemoglobin A1c": HealthDomain.ENDOCRINE,
        "Fasting Glucose": HealthDomain.ENDOCRINE,
        "Glucose": HealthDomain.ENDOCRINE,
        "Random Glucose": HealthDomain.ENDOCRINE,
        "Insulin": HealthDomain.ENDOCRINE,
        "C-Peptide": HealthDomain.ENDOCRINE,

        # Thyroid
        "TSH": HealthDomain.THYROID,
        "T3": HealthDomain.THYROID,
        "T4": HealthDomain.THYROID,
        "Free T4": HealthDomain.THYROID,
        "Free T3": HealthDomain.THYROID,

        # Lipid
        "Total Cholesterol": HealthDomain.LIPID,
        "HDL Cholesterol": HealthDomain.LIPID,
        "LDL Cholesterol": HealthDomain.LIPID,
        "Triglycerides": HealthDomain.LIPID,
        "VLDL": HealthDomain.LIPID,

        # Cardiovascular
        "Troponin": HealthDomain.CARDIOVASCULAR,
        "CK-MB": HealthDomain.CARDIOVASCULAR,
        "BNP": HealthDomain.CARDIOVASCULAR,
        "NT-proBNP": HealthDomain.CARDIOVASCULAR,

        # Hematology
        "Hemoglobin": HealthDomain.HEMATOLOGY,
        "Hematocrit": HealthDomain.HEMATOLOGY,
        "White Blood Cell Count": HealthDomain.HEMATOLOGY,
        "Red Blood Cell Count": HealthDomain.HEMATOLOGY,
        "Platelet Count": HealthDomain.HEMATOLOGY,
        "WBC": HealthDomain.HEMATOLOGY,
        "RBC": HealthDomain.HEMATOLOGY,

        # Liver
        "ALT": HealthDomain.LIVER,
        "AST": HealthDomain.LIVER,
        "ALP": HealthDomain.LIVER,
        "Bilirubin": HealthDomain.LIVER,
        "Total Bilirubin": HealthDomain.LIVER,
        "Direct Bilirubin": HealthDomain.LIVER,
        "GGT": HealthDomain.LIVER,
    }

    @classmethod
    def classify_lab_result(cls, lab_result: LabResult) -> HealthDomain:
        """Classify a single lab result into a health domain."""
        # Try exact match first
        if lab_result.test_name in cls.TEST_DOMAIN_MAP:
            return cls.TEST_DOMAIN_MAP[lab_result.test_name]

        # Try case-insensitive match
        for test_name, domain in cls.TEST_DOMAIN_MAP.items():
            if test_name.lower() == lab_result.test_name.lower():
                return domain

        # Try partial matching for common patterns
        test_lower = lab_result.test_name.lower()

        if any(keyword in test_lower for keyword in ["glucose", "a1c", "insulin"]):
            return HealthDomain.ENDOCRINE
        elif any(keyword in test_lower for keyword in ["creatinine", "gfr", "bun"]):
            return HealthDomain.RENAL
        elif any(keyword in test_lower for keyword in ["cholesterol", "triglyceride", "lipid"]):
            return HealthDomain.LIPID
        elif any(keyword in test_lower for keyword in ["hemoglobin", "hematocrit", "wbc", "rbc", "platelet"]):
            return HealthDomain.HEMATOLOGY
        elif any(keyword in test_lower for keyword in ["alt", "ast", "bilirubin", "liver"]):
            return HealthDomain.LIVER
        elif any(keyword in test_lower for keyword in ["tsh", "thyroid", "t3", "t4"]):
            return HealthDomain.THYROID

        return HealthDomain.OTHER

    @classmethod
    def classify_all_labs(cls, lab_results: List[LabResult]) -> List[LabResult]:
        """Classify all lab results and update their health_domain field."""
        for lab_result in lab_results:
            lab_result.health_domain = cls.classify_lab_result(lab_result)
        return lab_results

    @classmethod
    def group_by_domain(cls, lab_results: List[LabResult]) -> Dict[HealthDomain, List[LabResult]]:
        """Group lab results by health domain."""
        groups: Dict[HealthDomain, List[LabResult]] = {}

        for lab_result in lab_results:
            if lab_result.health_domain is None:
                lab_result.health_domain = cls.classify_lab_result(lab_result)

            domain = lab_result.health_domain
            if domain not in groups:
                groups[domain] = []
            groups[domain].append(lab_result)

        return groups
