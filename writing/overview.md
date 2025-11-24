---
slug: github-pmc-submission-writing-overview
id: github-pmc-submission-writing-overview
title: Exploring My PMC Submission Repo
repo: justin-napolitano/pmc-submission
githubUrl: https://github.com/justin-napolitano/pmc-submission
generatedAt: '2025-11-24T17:47:56.434Z'
source: github-auto
summary: >-
  I’ve put together a little project called [PMC
  Submission](https://github.com/justin-napolitano/pmc-submission). It’s my
  go-to collection for data analysis projects and technical interview solutions,
  primarily built using Jupyter Notebooks and Python, interfacing with Google
  Cloud services like BigQuery and Bigtable. If that interests you, let me walk
  you through it.
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: writing
entryLayout: writing
showInProjects: false
showInNotes: false
showInWriting: true
showInLogs: false
---

I’ve put together a little project called [PMC Submission](https://github.com/justin-napolitano/pmc-submission). It’s my go-to collection for data analysis projects and technical interview solutions, primarily built using Jupyter Notebooks and Python, interfacing with Google Cloud services like BigQuery and Bigtable. If that interests you, let me walk you through it.

## Why PMC Submission Exists

I built this repository as a personal portfolio. I wanted a place to gather my work on data analysis, especially around real-world datasets and problem-solving in Python. For me, it’s not just about practicing coding—it's about showcasing how I can leverage cloud technology to derive insights from data. 

By using tools like Jupyter Notebooks, I can present my thought processes and methodologies in a cleaner format. Plus, everything is tied to practical applications, making this more than just snippets of code.

## Key Design Decisions

A few core design choices shaped this repo:

- **Focus on Real Datasets**: The project centers around NYC taxi trip data and weather data, both of which allow me to perform significant analyses and simulations.
- **Google Cloud Integration**: Interfacing with BigQuery and Bigtable means I can handle large datasets efficiently. These tools not only boost performance but also expand my skills in managing cloud services.
- **Documentation Structure**: I opted for Jupyter Book to document my work. It provides a clear and navigable approach to showcase both code and explanations.

## Tech Stack

Here’s what I’m working with:

- **Python 3**: My primary language for this project.
- **Jupyter Notebook**: Great for interactive data analysis.
- **Google Cloud Services**: Mainly BigQuery for data analysis and Bigtable for storage.
- **Java**: I've included some Java samples for Bigtable external queries—it's there for experimentation.
- **Jupyter Book**: Used for creating organized documentation.

## Project Highlights

### Features

- **NYC Taxi Trip Analysis**: I’ve written SQL queries and Python scripts to dissect and analyze taxi data through BigQuery.
- **Weather Data Solutions**: Designed APIs for weather data collection and streaming, optimized with Google Cloud Bigtable.
- **Structured Interview Responses**: Jupyter Book serves as a home for my structured answers to technical interviews alongside models that calculate cost of living.
- **Automated Documentation Builds**: I’ve set up a pipeline to automate Jupyter Book documentation builds, which keeps everything up-to-date easily.

### Getting Started

If you’re interested in checking it out, the setup is straightforward:

1. **Clone the repo**:
   ```bash
   git clone https://github.com/justin-napolitano/pmc-submission.git
   cd pmc-submission
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Google Cloud credentials**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/creds.json"
   ```

Running the main Python script is as simple as:

```bash
python main.py
```

For BigQuery tests, poke around `test.py`, and to build those nice Jupyter Book docs, run:

```bash
python python_build.py
```

## Project Structure

Here’s a high-level view of how things are organized:

```
pmc-submission/
├── ch4-emissions/
├── jupyter-book/
│   ├── _config.yml
│   ├── _toc.yml
│   ├── notebooks/
│   ├── python_build.py
├── login.py
├── main.py
├── propensity_scoring/
├── query.py
├── query_gooogle.java
├── query_gooogle.json
├── test.py
└── documentation.ipynb
```

It’s modular enough to keep things manageable while being complex enough to challenge my skills.

## Trade-offs

Every project comes with trade-offs. One notable one here is the balance between simplicity and comprehensiveness. While I wanted users to easily run the analyses, detailed explanations could be overwhelming for some. I tried to keep it user-friendly while still providing enough insights.

I also dipped into Java, but that part isn't fully polished. It might leave some users confused about its intended use. Keep in mind, it's a work in progress.

## Future Work and Roadmap

There are a few things I'm itching to improve:

- **Code Refinement**: I want to tidy up that Java and Python BigQuery client code. Some parts feel messy.
- **Remove Duplicates**: Gotta clean up or consolidate those redundant files, especially `query_gooogle.json`.
- **Automated Testing**: I’m looking to expand CI/CD capabilities for the data pipelines. It’s crucial for reliability.
- **Documentation Enrichment**: I'd like to add more detailed usage examples to assist users better.
- **Data Ingestion Automation**: Streamlining the weather and taxi data workflows is a priority.
- **Error Handling Improvements**: Refine error handling and logging to make the scripts more robust.

This repo is an evolving canvas, and I’m keen on continually enhancing it.

If you want to stay up-to-date with what's happening here, feel free to follow me on my socials: Mastodon, Bluesky, and Twitter. I share my latest updates and thoughts there.

Thanks for taking the time to check out my PMC Submission project! I hope you find it as exciting as I do.
