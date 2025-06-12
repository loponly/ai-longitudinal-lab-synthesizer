"""LOINC mapping and biomarker normalization utilities."""
from typing import ClassVar, Dict, Optional

from src.models import LabResult, ReferenceRange


class LOINCMapper:
    """Maps lab test names to LOINC codes."""

    # Simplified LOINC mapping for common lab tests
    LOINC_MAP: ClassVar[Dict[str, str]] = {
        "HbA1c": "4548-4",
        "Hemoglobin A1c": "4548-4",
        "Creatinine": "2160-0",
        "Serum Creatinine": "2160-0",
        "eGFR": "33914-3",
        "Estimated GFR": "33914-3",
        "Fasting Glucose": "1558-6",
        "Glucose": "2345-7",
        "Total Cholesterol": "2093-3",
        "HDL Cholesterol": "2085-9",
        "LDL Cholesterol": "2089-1",
        "Triglycerides": "2571-8",
        "TSH": "3016-3",
        "BUN": "6299-2",
        "Hemoglobin": "718-7",
        "Hematocrit": "4544-3",
        "White Blood Cell Count": "6690-2",
        "Platelet Count": "777-3",
    }

    @classmethod
    def get_loinc_code(cls, test_name: str) -> Optional[str]:
        """Get LOINC code for a test name."""
        # Try exact match first
        if test_name in cls.LOINC_MAP:
            return cls.LOINC_MAP[test_name]

        # Try case-insensitive match
        for key, value in cls.LOINC_MAP.items():
            if key.lower() == test_name.lower():
                return value

        return None

    @classmethod
    def map_lab_result(cls, lab_result: LabResult) -> LabResult:
        """Add LOINC code to lab result."""
        loinc_code = cls.get_loinc_code(lab_result.test_name)
        if loinc_code:
            lab_result.loinc_code = loinc_code
        return lab_result


class BiomarkerNormalizer:
    """Normalizes biomarker values and provides reference ranges."""

    # Reference ranges for common lab tests
    REFERENCE_RANGES: ClassVar[Dict[str, ReferenceRange]] = {
        "HbA1c": ReferenceRange("HbA1c", 4.0, 5.6, "%"),
        "Hemoglobin A1c": ReferenceRange("Hemoglobin A1c", 4.0, 5.6, "%"),
        "Creatinine": ReferenceRange("Creatinine", 0.6, 1.3, "mg/dL"),
        "Serum Creatinine": ReferenceRange("Serum Creatinine", 0.6, 1.3, "mg/dL"),
        "eGFR": ReferenceRange("eGFR", 60, None, "mL/min/1.73m2"),
        "Estimated GFR": ReferenceRange("Estimated GFR", 60, None, "mL/min/1.73m2"),
        "Fasting Glucose": ReferenceRange("Fasting Glucose", 70, 99, "mg/dL"),
        "Glucose": ReferenceRange("Glucose", 70, 140, "mg/dL"),
        "Total Cholesterol": ReferenceRange("Total Cholesterol", None, 200, "mg/dL"),
        "HDL Cholesterol": ReferenceRange("HDL Cholesterol", 40, None, "mg/dL"),
        "LDL Cholesterol": ReferenceRange("LDL Cholesterol", None, 100, "mg/dL"),
        "Triglycerides": ReferenceRange("Triglycerides", None, 150, "mg/dL"),
        "TSH": ReferenceRange("TSH", 0.4, 4.0, "mIU/L"),
        "BUN": ReferenceRange("BUN", 7, 20, "mg/dL"),
        "Hemoglobin": ReferenceRange("Hemoglobin", 12.0, 16.0, "g/dL"),
        "Hematocrit": ReferenceRange("Hematocrit", 36.0, 46.0, "%"),
        "White Blood Cell Count": ReferenceRange("White Blood Cell Count", 4.5, 11.0, "K/uL"),
        "Platelet Count": ReferenceRange("Platelet Count", 150, 450, "K/uL"),
    }

    @classmethod
    def get_reference_range(cls, test_name: str) -> Optional[ReferenceRange]:
        """Get reference range for a test."""
        # Try exact match first
        if test_name in cls.REFERENCE_RANGES:
            return cls.REFERENCE_RANGES[test_name]

        # Try case-insensitive match
        for key, value in cls.REFERENCE_RANGES.items():
            if key.lower() == test_name.lower():
                return value

        return None

    @classmethod
    def normalize_lab_result(cls, lab_result: LabResult) -> LabResult:
        """Add reference range and status to lab result."""
        ref_range = cls.get_reference_range(lab_result.test_name)
        if ref_range:
            # Format reference range string
            min_str = str(ref_range.min_value) if ref_range.min_value is not None else ""
            max_str = str(ref_range.max_value) if ref_range.max_value is not None else ""

            if min_str and max_str:
                lab_result.reference_range = f"Normal: {min_str}-{max_str}"
            elif min_str:
                lab_result.reference_range = f"Normal: >{min_str}"
            elif max_str:
                lab_result.reference_range = f"Normal: <{max_str}"

        return lab_result

    @classmethod
    def get_status_indicator(cls, lab_result: LabResult) -> str:
        """Get status indicator (↑, ↓, or empty) for a lab result."""
        ref_range = cls.get_reference_range(lab_result.test_name)
        if ref_range:
            return ref_range.get_status(lab_result.value)
        return ""
