
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

## 🧰 Tech Stack

- **Langroid**, **loinc-tools**, **TSFresh**
- **pdfplumber**, **PyMuPDF**
- **pytest**, **Docker**, **Streamlit**
- **UCUM units**, **pandoc**, **Flask API**

## 📦 Deployment

```bash
docker-compose up --build
```

## 🔐 Privacy

Simulated HIPAA/GDPR-compliant data flow with PHI leakage detection.

---

© 2025 – AI Clinical Synth Labs
