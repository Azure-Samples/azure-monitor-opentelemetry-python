---
page_type: sample
languages:
- python
- html
products:
- azure
description: "This sample contains a simple Django application to show a common distributed tracing scenario."
urlFragment: azure-monitor-opentelemetry-d
---

# HTTP Application

## Setup

1. This package is not hosted on Pypi. You can install all dependencies locally using `pip install -r azure_monitor/http_sample/requirements.txt`.
2. To send telemetry to Azure Monitor, populate `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable with your connection string.
3. Install required libraries through `requirements.txt`.

```
pip install -r requirements.txt
```

## Usage

1. Navigate to where `azure_monitor\http_sample` is located.
2. Start the django application via `python manage.py runserver`. Your application will be running on port 8000.
3. Start a local http webserver by running `python third.py`. This webserver will be listening to port 8080.
4. To start the beginning of the trace, run `python first.py`. The logical calling will be `first.py` -> `django app` -> `third.py`.
You should see this reflected in your application map in Azure monitor.
