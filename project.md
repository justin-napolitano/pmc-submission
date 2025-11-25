---
slug: github-pmc-submission
id: github-pmc-submission
title: Data Analysis Projects with Google Cloud and Python
repo: justin-napolitano/pmc-submission
githubUrl: https://github.com/justin-napolitano/pmc-submission
generatedAt: '2025-11-24T21:35:53.810Z'
source: github-auto
summary: >-
  Explore a collection of data analysis projects using Python, Jupyter Notebooks, and Google Cloud
  services like BigQuery and Bigtable.
tags:
  - python
  - jupyter notebook
  - google cloud
  - bigquery
  - bigtable
  - data analysis
  - ci/cd
  - api integration
seoPrimaryKeyword: data analysis with google cloud
seoSecondaryKeywords:
  - jupyter book documentation
  - nyc taxi data analysis
  - weather data streaming
  - automated testing for data pipelines
  - python scripts for bigquery
seoOptimized: true
topicFamily: datascience
topicFamilyConfidence: 0.9
kind: project
entryLayout: project
showInProjects: true
showInNotes: false
showInWriting: false
showInLogs: false
---

A collection of data analysis projects and technical interview solutions by Justin Napolitano, primarily using Jupyter Notebooks and Python scripts interfacing with Google Cloud services such as BigQuery and Bigtable.

## Features

- SQL queries and Python scripts for analyzing NYC taxi trip data using BigQuery.
- Weather data collection and streaming solutions using APIs and Google Cloud Bigtable.
- Jupyter Book structured technical interview answers and cost of living models.
- Automated build pipeline for Jupyter Book documentation.

## Tech Stack

- Python 3
- Jupyter Notebook
- Google Cloud BigQuery and Bigtable
- Java (sample Bigtable external query)
- Jupyter Book for documentation

## Getting Started

### Prerequisites

- Python 3 installed
- Google Cloud SDK configured with appropriate credentials
- `pip` for Python package management

### Installation

1. Clone the repository:

```bash
git clone https://github.com/justin-napolitano/pmc-submission.git
cd pmc-submission
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set Google Cloud credentials environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/creds.json"
```

### Running

- To run the main Python script:

```bash
python main.py
```

- To run test queries against BigQuery, explore `test.py`.

- To build the Jupyter Book documentation:

```bash
python python_build.py
```

## Project Structure

```
pmc-submission/
├── ch4-emissions/                 # Folder likely related to methane emissions analysis
├── jupyter-book/                  # Jupyter Book source and build files
│   ├── _config.yml                # Jupyter Book configuration
│   ├── _toc.yml                   # Table of contents
│   ├── notebooks/                 # Markdown and notebooks for interview and analysis
│   ├── python_build.py            # Build automation for Jupyter Book
├── login.py                      # Google Cloud Bigtable login helper
├── main.py                       # Main entry point
├── propensity_scoring/           # Folder likely containing propensity scoring analysis
├── python_build.py               # Build automation for main project
├── query.py                      # Java-like imports, possibly incomplete BigQuery client code
├── query_gooogle.java            # Java sample for Bigtable external query
├── query_gooogle.json            # Duplicate of java file, likely misplaced
├── test.py                      # Python scripts with BigQuery SQL queries
└── documentation.ipynb           # Possibly project documentation notebook
```

## Future Work / Roadmap

- Complete and clean up Java and Python BigQuery client code.
- Consolidate or remove duplicate/misplaced files like `query_gooogle.json`.
- Expand automated testing and CI/CD for data pipelines.
- Enhance documentation with more detailed usage examples.
- Integrate data pipeline automation for weather and taxi data ingestion.
- Improve error handling and logging in scripts.

---

*Assumptions: The project is a personal portfolio of data analysis and technical interview work using Google Cloud services. Some files appear incomplete or duplicated, suggesting ongoing development.*

