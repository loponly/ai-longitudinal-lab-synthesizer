# ai-longitudinal-lab-synthesizer

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

- LOINC mapping & biomarker normalization
- Health-area assignment with Langroid agents
- Longitudinal clustering & anomaly detection
- PDF parsing and LaTeX/Markdown generation
- PHI detection & logging for HIPAA/GDPR compliance
- Unit-tested pipelines and CHR run tracing

## 🧱 Code Standards

- ✅ SOLID Principles
- 🎯 Clean Architecture (modular, testable)
- 🧪 90%+ test coverage via pytest
- 🧼 Lint: ruff / Format: black / Type-check: mypy
- 📖 Every function/class must include type hints and docstrings
- 🔒 Secure (no secrets in code, validate all inputs)

Run locally:
```bash
black src/ tests/
ruff src/ tests/
mypy src/
pytest

## 🧰 Tech Stack

- **Langroid**, **TSFresh**
- **pdfplumber**, **PyMuPDF**
- **pytest**, **Docker**, **Streamlit**
- **UCUM units**, **pandoc**, **Flask API**

## 📦 Deployment

```bash
docker-compose up --build
```

## 🔐 Privacy

Simulated HIPAA/GDPR-compliant data flow with PHI leakage detection.

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
Below is a minimal example of using Langroid to assign health areas to lab results:

```python
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.language_models.openai_gpt import OpenAIChatModel, OpenAIGPTConfig

config = ChatAgentConfig(
    llm=OpenAIGPTConfig(chat_model=OpenAIChatModel.GPT4o),
    vecdb=None,
)

agent = ChatAgent(config)

# System message instructs the agent to classify labs by health area
tag = "renal"  # Example tag, could be dynamic
system_message = f"""
You are a clinical lab classifier. Assign each lab result to a health area (e.g., renal, endocrine).
Respond with the health area for: Creatinine, eGFR, HbA1c, Fasting Glucose.
"""
agent.set_system_message(system_message)

response = agent.chat("Creatinine: 1.6 mg/dL, eGFR: 54, HbA1c: 7.2%, Fasting Glucose: 120 mg/dL")
print(response)
```

### Building Agent Trees
For more complex logic, you can compose agents in a tree structure, where each agent handles a sub-task and passes results to others. See [docs/langroid/examples/agent-tree.md](docs/langroid/examples/agent-tree.md) for a detailed example.

### References
- [Langroid Quick Start](docs/langroid/quick-start/index.md)
- [Agent Tree Example](docs/langroid/examples/agent-tree.md)
- [Langroid Documentation](https://langroid.github.io/langroid/)

---

© 2025 – AI Clinical Synth Labs
