---
slug: github-pmc-submission
title: Data Analysis and Ingestion with BigQuery and Bigtable on Google Cloud
repo: justin-napolitano/pmc-submission
githubUrl: https://github.com/justin-napolitano/pmc-submission
generatedAt: '2025-11-23T09:24:38.257102Z'
source: github-auto
summary: >-
  Overview of querying NYC taxi data with BigQuery, scalable weather data ingestion via Bigtable,
  and Jupyter Book documentation automation.
tags:
  - bigquery
  - bigtable
  - google-cloud
  - data-ingestion
  - jupyter-book
  - python
seoPrimaryKeyword: bigquery
seoSecondaryKeywords:
  - bigtable
  - data ingestion
  - google cloud
  - jupyter book
seoOptimized: true
---

# PMC Submission: Technical Overview and Implementation Notes

This repository aggregates a series of data analysis projects and technical interview solutions centered around data ingestion, processing, and querying using Google Cloud services. The primary focus is on leveraging BigQuery for large-scale SQL analytics and Bigtable for scalable NoSQL data storage.

## Motivation

The project serves as both a personal portfolio and a technical demonstration of skills relevant to data analyst and data engineer roles. It addresses common data challenges such as querying large public datasets, building data ingestion pipelines, and structuring reproducible documentation.

## Problem Statement

- How to efficiently query and analyze large-scale taxi trip data from NYC's public BigQuery dataset.
- How to collect and store weather data from APIs at scale, considering both batch CSV and streaming Bigtable approaches.
- How to organize technical interview answers and data models in a reproducible and presentable format.

## Architecture and Components

### BigQuery Analysis

Python scripts (`test.py`, notebooks under `jupyter-book/notebooks/`) interact with the Google BigQuery API to run SQL queries on the `nyc-tlc.green.trips_2015` dataset. These queries address:

- Monthly passenger counts and total amounts.
- Average hourly ridership.
- Trip duration and fare analysis.

The scripts use the `google.cloud.bigquery` client with result fetching and conversion to pandas DataFrames for further analysis.

### Weather Data Collection

Two approaches are presented:

1. **CSV-based batch ingestion:** Using API calls to OpenWeatherMap, data is collected periodically and appended to CSV files partitioned by hour. This method is simple but poses challenges at scale, such as file corruption and asynchronous call management.

2. **Streaming via Bigtable:** A more scalable approach writes weather data directly to Google Cloud Bigtable, reducing file management complexity. Data can then be migrated to a relational database like PostgreSQL for long-term storage and querying.

### Jupyter Book Documentation

The repository uses Jupyter Book to organize and present technical interview answers, cost of living models, and other analyses. The book is configured to force notebook execution on build, ensuring up-to-date outputs.

A build automation script (`python_build.py`) handles dependency installation, cleaning, building, committing, and pushing the book.

### Code Samples and Tools

- `login.py` abstracts Google Cloud Bigtable client instantiation.
- `main.py` serves as an entry point, currently initializing a Bigtable client.
- Java code samples demonstrate querying external Bigtable data sources via temporary tables, indicating familiarity with multi-language environments.

## Implementation Details

- SQL queries use standard BigQuery syntax, with date truncation, aggregation, and window functions.
- Python scripts rely on the `google-cloud-bigquery` library and pandas for data handling.
- The build pipeline uses subprocess calls to `jupyter-book` CLI commands for cleaning and building documentation.
- The weather data ingestion solution considers practical aspects of asynchronous API calls and large data volumes.

## Practical Considerations

- Environment setup requires Google Cloud credentials and Python dependencies.
- Some code files appear incomplete or duplicated (e.g., `query_gooogle.json`), suggesting ongoing development.
- Error handling and logging are minimal and could be improved for production readiness.
- The repository blends exploratory analysis, technical interview preparation, and build automation, reflecting a comprehensive approach to data projects.

## Summary

This project exemplifies a pragmatic approach to data analysis and engineering challenges using Google Cloud technologies. It balances exploratory SQL analytics, scalable data ingestion strategies, and structured documentation. The codebase serves as a reference for implementing data pipelines, querying large datasets, and organizing technical content for presentation and review.
