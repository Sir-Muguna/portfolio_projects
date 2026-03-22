```markdown
# Tech Education Analysis Project

This project performs a comprehensive analysis of student feedback on tech education and explores emerging trends in biotech and health using NLP.

## Project Overview

The analysis is driven by data extracted from student survey responses and external text corpora, combining statistical tests, natural language processing (NLP), and visualization to deliver actionable insights for educational stakeholders and industry partners.

---

## Setup Instructions

### 1. Set Up a Virtual Environment

To avoid dependency conflicts, it's recommended to create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## Workflow Steps

### 📥 Data Acquisition

- Python scripts are used to download survey CSV files directly from Google Drive using file IDs.

### 🧹 Data Cleaning & Processing

- Missing values, data types, and formatting are handled.
- Survey fields are transformed for consistent analysis.

### 📊 Statistical Analysis

- Key statistical tests include:
  - T-tests (industrial training)
  - Wilcoxon Signed-Rank Test (lecture satisfaction)
  - Chi-square Test (course relevance)

### 🧠 NLP & Tech Trends Analysis

- Named Entity Recognition (NER) is applied to biotech/health-related text.
- Emerging trends and key entities (people, organizations, locations) are identified.

---

## Output

- A professional report summarizing the insights is generated and exported in `.docx` format.
- Visualizations and summaries support data-driven decision-making.

---
```
