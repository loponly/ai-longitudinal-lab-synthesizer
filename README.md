# ai-longitudinal-lab-synthesizer

[![Test and Coverage](https://github.com/loponly/ai-longitudinal-lab-synthesizer/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/loponly/ai-longitudinal-lab-synthesizer/actions/workflows/test-coverage.yml)



[![codecov](https://codecov.io/gh/loponly/ai-longitudinal-lab-synthesizer/graph/badge.svg?token=WQ752UURHY)](https://codecov.io/gh/loponly/ai-longitudinal-lab-synthesizer)




🧪 AI-Driven Longitudinal Lab Report Synthesizer

This project synthesizes de-identified lab data into clinically relevant health summaries, supporting biomarker normalization, LOINC mapping, health-area classification, and LaTeX/Markdown rendering. It includes agent-based orchestration using Langroid, unit testing, and PDF parser configuration with privacy compliance.

## 🔍 Example Input

```json
{
  "patient_id": "PT123456",
  "labs": [
    {
      "test_name": "HbA1c",
      "value": 7.2,
      "unit": "%",
      "date": "2023-11-01"
    },
    {
      "test_name": "Creatinine",
      "value": 1.6,
      "unit": "mg/dL",
      "date": "2023-11-01"
    },
    {
      "test_name": "eGFR",
      "value": 54,
      "unit": "mL/min/1.73m2",
      "date": "2023-11-01"
    },
    {
      "test_name": "Fasting Glucose",
      "value": 120,
      "unit": "mg/dL",
      "date": "2023-11-01"
    }
  ]
}
```

## 📄 Example Output

```markdown
## Patient Summary – ID: PT123456

**Health Domain: Renal**
- **Creatinine**: 1.6 mg/dL ↑ (Normal: 0.6–1.3)
- **eGFR**: 54 mL/min/1.73m² ↓
- **Trend**: 12% decline over 90 days – suggest CKD stage 2

**Endocrinology**
- **HbA1c**: 7.2% ↑ (Pre-Diabetic > 6.5%)
- **Fasting Glucose**: 120 mg/dL ↑

🧠 **Summary**: Patient trending toward early CKD and pre-diabetes. Recommend follow-up testing and nephrology referral.
```

## 🧠 Key Features

- **LOINC Mapping & Biomarker Normalization**: Automated mapping of lab tests to LOINC codes with reference range validation
- **AI-Powered Health Classification**: Langroid agents classify lab results into health domains (Renal, Endocrine, Lipid, etc.)
- **Clinical Trend Analysis**: Intelligent analysis of longitudinal lab data with clinical recommendations
- **Multi-Format Report Generation**: Output in Markdown, LaTeX, and JSON formats
- **Comprehensive Test Coverage**: 90%+ test coverage with pytest across all modules
- **Reference Range Validation**: Automatic status indicators (↑/↓) based on clinical reference ranges
- **Agent-Based Orchestration**: Langroid agents for classification, trend analysis, and report generation
- **Modular Architecture**: Clean separation of concerns with dedicated modules for each functionality

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### 1. Clone the repository
```bash
git clone <repository-url>
cd ai-longitudinal-lab-synthesizer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Replace 'sk-proj-' with your actual OpenAI API key
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### 4. Run the application
```bash
# Run the main demo
python main.py

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/

# Format and lint code
black src/ tests/
ruff src/ tests/
mypy src/
```

## 🚀 Getting Started

### Quick Usage Example

```python
from src.synthesizer import LabDataSynthesizer

# Initialize the synthesizer
synthesizer = LabDataSynthesizer()

# Prepare your lab data
lab_data = {
    "patient_id": "PT123456",
    "labs": [
        {"test_name": "HbA1c", "value": 7.2, "unit": "%", "date": "2023-11-01"},
        {"test_name": "Creatinine", "value": 1.6, "unit": "mg/dL", "date": "2023-11-01"},
        {"test_name": "eGFR", "value": 54, "unit": "mL/min/1.73m2", "date": "2023-11-01"}
    ]
}

# Generate reports in multiple formats
results = synthesizer.synthesize_to_formats(lab_data)

print("Markdown Report:")
print(results["markdown"])

print("\nJSON Report:")
print(results["json"])

# Access the structured patient summary
patient_summary = results["patient_summary"]
for health_summary in patient_summary.health_summaries:
    print(f"\n{health_summary.domain.value} Domain:")
    print(f"Trends: {health_summary.trends}")
```

### Expected Output

The system will generate comprehensive reports like:

```markdown
## Patient Summary - ID: PT123456

**Health Domain: Renal**
- **Creatinine**: 1.6 mg/dL ↑ (Normal: 0.6-1.3)
- **eGFR**: 54 mL/min/1.73m² ↓ (Normal: >60)
- **Trend**: Moderate kidney dysfunction (Stage 3a CKD) - monitor renal function

**Health Domain: Endocrine**
- **HbA1c**: 7.2% ↑ (Normal: 4.0-5.6)
- **Trend**: Borderline diabetes control - optimize diabetes therapy

🧠 **Summary**: Patient trending toward early CKD and suboptimal diabetes control. Recommend nephrology referral and diabetes management optimization.
```

## 🧱 Code Standards

- ✅ SOLID Principles
- 🎯 Clean Architecture (modular, testable)
- 🧪 90%+ test coverage via pytest
- 🧼 Lint: ruff / Format: black / Type-check: mypy
- 📖 Every function/class must include type hints and docstrings
- 🔒 Secure (no secrets in code, validate all inputs)

## 🧰 Tech Stack

- **AI/ML**: Langroid (agent orchestration), OpenAI GPT-4o-mini
- **Data Processing**: pandas, numpy, python-dotenv
- **Testing**: pytest, pytest-mock, pytest-cov
- **Code Quality**: black (formatter), ruff (linter), mypy (type checker)
- **Documentation**: Comprehensive docs for PyMuPDF, pdfplumber, tsfresh, Langroid
- **Report Generation**: Markdown, LaTeX, JSON output formats
- **Development**: Python 3.8+, modular architecture with SOLID principles

## 📁 Project Structure

```
src/
├── models.py              # Data models (LabResult, PatientData, HealthSummary)
├── health_classifier.py   # Rule-based health domain classification
├── loinc_mapping.py       # LOINC codes and reference ranges
├── trend_analyzer.py      # Clinical trend analysis and recommendations
├── report_generator.py    # Multi-format report generation
├── synthesizer.py         # Main orchestrator with Langroid agents
└── __init__.py

tests/
├── test_basic.py          # Basic functionality tests
├── test_health_classifier.py  # Health classification tests
├── test_loinc_mapping.py  # LOINC mapping tests
├── test_models.py         # Data model tests
├── test_report_generator.py   # Report generation tests
├── test_synthesizer.py    # Main synthesizer tests
├── test_trend_analyzer.py # Trend analysis tests
├── test_integration.py    # End-to-end integration tests
└── __init__.py
```

## 📊 Health Domains Supported

The system classifies lab results into the following clinical domains:

- **RENAL**: Creatinine, eGFR, BUN, Albumin, Protein
- **ENDOCRINE**: HbA1c, Glucose, Insulin, C-Peptide
- **LIPID**: Total/HDL/LDL Cholesterol, Triglycerides
- **THYROID**: TSH, T3, T4, Free T4, Free T3
- **HEMATOLOGY**: Hemoglobin, Hematocrit, WBC, RBC, Platelets
- **LIVER**: ALT, AST, ALP, Bilirubin, GGT
- **CARDIOVASCULAR**: Troponin, CK-MB, BNP, NT-proBNP
- **OTHER**: Unclassified or rare tests

## 🏗️ Architecture Overview

### Agent-Based Processing Pipeline

1. **Input Processing**: Parse JSON lab data into `PatientData` objects
2. **LOINC Mapping**: Map test names to standardized LOINC codes
3. **Reference Range Validation**: Apply clinical reference ranges and status indicators
4. **AI Classification**: Langroid agents classify labs into health domains
5. **Trend Analysis**: Clinical analysis with recommendations using specialized agents
6. **Report Generation**: Multi-format output (Markdown, LaTeX, JSON)

### Key Classes

- **`LabDataSynthesizer`**: Main orchestrator with Langroid agent integration
- **`HealthAreaClassifier`**: Rule-based classification into health domains
- **`BiomarkerNormalizer`**: Reference range validation and status indicators
- **`TrendAnalyzer`**: Clinical trend analysis with domain-specific logic
- **`ReportGenerator`**: Multi-format report generation

### Langroid Agents

- **LabClassifier Agent**: Intelligent lab result classification
- **TrendAnalyzer Agent**: Longitudinal trend analysis
- **ReportGenerator Agent**: Enhanced markdown report generation

## 🔐 Privacy

Simulated HIPAA/GDPR-compliant data flow with PHI leakage detection.

## 🩺 Clinical Logic & Reference Ranges

The system includes comprehensive clinical logic with evidence-based reference ranges:

### Renal Function Analysis
- **Creatinine**: Normal 0.6-1.3 mg/dL
- **eGFR**: Normal >60 mL/min/1.73m², CKD staging at <60, <45, <30
- **BUN**: Normal 7-20 mg/dL
- Automated CKD stage assessment and nephrology referral recommendations

### Diabetes & Endocrine
- **HbA1c**: Normal <5.7%, Pre-diabetes 5.7-6.4%, Diabetes ≥6.5%
- **Fasting Glucose**: Normal 70-99 mg/dL, Impaired 100-125 mg/dL, Diabetes ≥126 mg/dL
- Diabetes control assessment with management recommendations

### Lipid Management
- **Total Cholesterol**: Target <200 mg/dL
- **LDL**: Target <100 mg/dL (varies by risk)
- **HDL**: Target >40 mg/dL
- **Triglycerides**: Target <150 mg/dL
- Cardiovascular risk stratification

### Clinical Decision Support
- Trend analysis with percentage changes over time
- Automated clinical recommendations
- Disease progression tracking
- Treatment intensification suggestions

## 🤖 Agentic Logic with Langroid

This project uses [Langroid](https://github.com/langroid/langroid) to orchestrate agent-based workflows for lab data synthesis and health-area assignment.

### What is Agentic Logic?
Agentic logic means breaking down complex tasks into modular, interacting agents—each responsible for a specific sub-task. In this project, Langroid agents handle tasks like LOINC mapping, biomarker normalization, and health-area classification, enabling flexible, explainable, and extensible pipelines.

### Installing Langroid

```bash
pip install langroid
```

For document parsing and advanced features:

```bash
pip install "langroid[doc-chat]"
```

### Example: Health-Area Assignment Agent
Below is how the actual system uses Langroid for lab classification:

```python
from langroid import ChatAgent, ChatAgentConfig, Task
from langroid.language_models import OpenAIGPTConfig

# Initialize the classification agent (as used in synthesizer.py)
classifier_agent = ChatAgent(
    ChatAgentConfig(
        name="LabClassifier",
        llm=OpenAIGPTConfig(chat_model="gpt-4o-mini"),
        system_message="""
        You are a medical lab classification expert. Your role is to:
        1. Analyze lab test results and classify them into health domains
        2. Identify abnormal values based on reference ranges
        3. Determine clinical significance of results
        
        Health domains include: RENAL, ENDOCRINE, LIPID, HEPATIC, HEMATOLOGIC, CARDIAC, OTHER
        
        For each lab result, provide:
        - Health domain classification
        - Normal/abnormal status with direction (↑/↓)
        - Clinical interpretation
        """,
    )
)

# Create and run a classification task
classification_task = Task(
    classifier_agent,
    name="classify_labs",
    system_message="Classify the following lab results into health domains:",
)

lab_data = """
- HbA1c: 7.2 % (Normal: 4.0-5.6) [2023-11-01]
- Creatinine: 1.6 mg/dL (Normal: 0.6-1.3) [2023-11-01]
- eGFR: 54 mL/min/1.73m2 (Normal: >60) [2023-11-01]
"""

result = classification_task.run(lab_data)
print(result.content)
```

### Building Agent Trees
For more complex logic, you can compose agents in a tree structure, where each agent handles a sub-task and passes results to others. See [docs/langroid/examples/agent-tree.md](docs/langroid/examples/agent-tree.md) for a detailed example.

### References
- [Langroid Quick Start](docs/langroid/quick-start/index.md)
- [Agent Tree Example](docs/langroid/examples/agent-tree.md)
- [Langroid Documentation](https://langroid.github.io/langroid/)

## 👤 Author

**Enkhbat E**  
📧 Email: enkhbat@em4it.com

---

© 2025 – AI Clinical Synth Labs
