---
page_type: sample
languages:
- python
- html
products:
- azure
description: "This sample contains a simple application that shows a common distributed tracing scenario using a database."
urlFragment: azure-monitor-opentelemetry-d
---

# Database sample application

## Setup

1. This package is not hosted on Pypi. You can install all dependencies locally using `pip install -r azure_monitor/db_sample/requirements.txt`.
2. To send telemetry to Azure Monitor, populate `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable with your connection string.
3. Install required libraries through `requirements.txt`.

```
pip install -r requirements.txt
```
4. This sample uses a postgresql database. Follow these [steps](https://www.postgresql.org/docs/10/installation.html) to get postgresql onto your machine.

## Usage

1. Create a database called `test` with user `postgres` and password `password`.
2. Run `sample.py`. The changes are not committed so the commands will not persist in the database, but the telemetry will be generated.
