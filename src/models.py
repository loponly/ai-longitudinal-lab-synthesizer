"""Data models for lab results and patient data."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class HealthDomain(Enum):
    """Health domains for lab result classification."""

    RENAL = "Renal"
    ENDOCRINE = "Endocrine"
    CARDIOVASCULAR = "Cardiovascular"
    HEMATOLOGY = "Hematology"
    LIVER = "Liver"
    LIPID = "Lipid"
    THYROID = "Thyroid"
    IMMUNOLOGY = "Immunology"
    OTHER = "Other"


@dataclass
class LabResult:
    """Individual lab test result."""

    test_name: str
    value: float
    unit: str
    date: str
    loinc_code: Optional[str] = None
    reference_range: Optional[str] = None
    health_domain: Optional[HealthDomain] = None

    def __post_init__(self) -> None:
        """Validate and normalize data after initialization."""
        if isinstance(self.date, str):
            # Keep as string for simplicity, but validate format
            try:
                datetime.strptime(self.date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format: {self.date}. Expected YYYY-MM-DD")


@dataclass
class PatientData:
    """Patient lab data collection."""

    patient_id: str
    labs: List[LabResult]

    def __post_init__(self) -> None:
        """Convert dict labs to LabResult objects if needed."""
        converted_labs = []
        for lab in self.labs:
            if isinstance(lab, dict):
                converted_labs.append(LabResult(**lab))
            else:
                converted_labs.append(lab)
        self.labs = converted_labs


@dataclass
class ReferenceRange:
    """Reference ranges for lab values."""

    test_name: str
    min_value: Optional[float]
    max_value: Optional[float]
    unit: str
    population: str = "adult"

    def is_normal(self, value: float) -> bool:
        """Check if a value is within normal range."""
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def get_status(self, value: float) -> str:
        """Get status indicator (↑, ↓, or normal)."""
        if self.is_normal(value):
            return ""
        elif self.min_value is not None and value < self.min_value:
            return "↓"
        elif self.max_value is not None and value > self.max_value:
            return "↑"
        return ""


@dataclass
class HealthSummary:
    """Health domain summary for a patient."""

    domain: HealthDomain
    lab_results: List[LabResult]
    trends: Optional[str] = None
    recommendations: Optional[str] = None


@dataclass
class PatientSummary:
    """Complete patient health summary."""

    patient_id: str
    health_summaries: List[HealthSummary]
    overall_summary: Optional[str] = None
