---
slug: github-pmc-submission-note-technical-overview
id: github-pmc-submission-note-technical-overview
title: PMC Submission Overview
repo: justin-napolitano/pmc-submission
githubUrl: https://github.com/justin-napolitano/pmc-submission
generatedAt: '2025-11-24T18:42:57.158Z'
source: github-auto
summary: >-
  The **pmc-submission** repo contains data analysis projects and technical
  interview solutions. I mainly use **Python** and **Jupyter Notebooks** with
  **Google Cloud** services like BigQuery and Bigtable.
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: note
entryLayout: note
showInProjects: false
showInNotes: true
showInWriting: false
showInLogs: false
---

The **pmc-submission** repo contains data analysis projects and technical interview solutions. I mainly use **Python** and **Jupyter Notebooks** with **Google Cloud** services like BigQuery and Bigtable.

### Key Features:

- Analyze NYC taxi trip data with SQL queries and Python scripts in BigQuery.
- Stream weather data using APIs and Bigtable.
- Jupyter Book format for interview answers and cost of living models.
- Automated pipeline for building Jupyter Book docs.

### Quick Start:

1. Clone the repo:

   ```bash
   git clone https://github.com/justin-napolitano/pmc-submission.git
   cd pmc-submission
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your Google Cloud credentials:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/creds.json"
   ```

### Important Notes:

- Use `python main.py` to run the main script.
- Check `test.py` for SQL queries against BigQuery.
- Clean up or consolidate duplicate files as needed.
