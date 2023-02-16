# Analytis Engineering

## Intro to Analytics Engineering

- What is Analytics Engineering
  - Data Engineer: prepares and maintains the infrastructure the data team needs
  - Data Analyst: Uses data to solve and answer questions
  - Analytics Engineer: bridges the gap between DE and DA. Introduces software engineering to data analyists and data scientist.
- ETL vs ELT

| ETL | ELT |
| --- | --- |
| Slightly more stable and compliant data analysis | Faster and more flexible data analysis |
| Higher storage and compute costs | Lower cost and maintenance |

- Kimball's Dimensional Modeling
  - Objective
    - Deliver data understandable to the business users
    - Deliver fast query performance
  - Approach
    - Prioritise user understandability and query performance over non redundant data (3NF)
  - Other approaches
    - Bill Inmon
    - Data valut
- Elements of Dimensional Modeling
  - Facts tables
    - Measurements, metrics or facts
    - Corresponds to a business process
    - "verbs"
  - Dimensions tables
    - Corresponds to a business entity
    - Provides context to a business process
    - "nouns"
- Architecture of Dimensional Modeling
  - Stage area
    - contains raw data
    - Not meant to be exposed to everyone
  - Processing data
    - From raw data to data models
    - Focuses in efficiency
    - Ensuring standards
  - Presentation area
    - Final presentation of the data
    - Exposure to business stakeholder

## DBT

- What is DBT
  - Data Build Tool
  - Helps with transformation
  - Introduces good software development practices
    - modularity
    - portability
    - CI/CD
    - documentation
- How to use dbt
  - dbt Core
    - open source project that allows data transformation
    - builds and runs a dbt project files
    - includes sql compilation logic, macros and database adapters
    - includes a CLI interface to run dbt commands locally
  - dbt Cloud
    - SaaS application to develop and manage dbt projects
    - Web-based IDE to develop and run any project
    - Jobs orchestration
    - Logging and Alerting
    - Integrated documentation
