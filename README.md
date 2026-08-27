# ITDR Generic Data Ingestion Framework

A generic data ingestion framework built using FastAPI and PostgreSQL.

The framework accepts ITDR/security event data from different source systems and supports multiple input formats and database operations.

## Features

- FastAPI-based REST API
- Generic data ingestion
- Supports JSON, CSV and XML files
- Data normalization
- Raw data preservation
- PostgreSQL database integration
- Supports multiple database operations:
  - INSERT
  - APPEND
  - TRUNCATE
  - UPSERT
- Automatic event ID generation
- Duplicate event handling through event ID
- Swagger UI for API testing

## Supported File Formats

The framework currently supports:

- JSON
- CSV
- XML

Example source systems:

- Microsoft Entra ID
- AWS
- Azure
- Other security/ITDR systems

The framework is designed to accept different source formats and convert them into a common structure.

## Architecture

```text
Source System
     |
     v
JSON / CSV / XML
     |
     v
FastAPI
     |
     v
Parser
     |
     v
Normalizer
     |
     v
Database Operation
     |
     +---- INSERT
     |
     +---- APPEND
     |
     +---- TRUNCATE
     |
     +---- UPSERT
     |
     v
PostgreSQL