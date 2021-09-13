---
page_type: sample
languages:
- python
- html
products:
- azure
description: "This sample contains a simple Flask application to show how you can instrument the OpenTelemetry Azure Monitor exporters as well as track telemetry from popular Python libraries via OpenTelemetry instrumentations."
urlFragment: azure-monitor-opentelemetry-d
---

# Flask "To-Do" Sample Application

## Setup

1. This package is not hosted on Pypi. You can install all dependencies locally using `pip install -r azure_monitor/flask_sample/requirements.txt`.
2. To send telemetry to Azure Monitor, modify your connection string field in `config.py` or populate `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable.

```
CONNECTION_STRING = <your-cs-here>
```

The default database URI links to a sqlite database `app.db`. To configure a different database, you can modify `config.py` and change the `SQLALCHEMY_DATABASE_URI` value to point to a database of your choosing.

```
SQLALCHEMY_DATABASE_URI = <your-database-URI-here>
```
3. Install required libraries through `requirements.txt`.

```
pip install -r requirements.txt
```

## Usage

1. Navigate to where `azure_monitor\flask_sample` is located.
2. Run the main application via `python sample.py`.
4. Hit your local endpoint (should be http://localhost:5000). This should open up a browser to the main page.
5. On the newly opened page, you can add tasks via the textbox under `Add a new todo item:`. You can enter any text you want (cannot be blank).
6. Click `Add Item` to add the task. The task will be added under `Incomplete Items`. Adding an item with greater than 10 characters will generate an error.
7. To utilize the `Save to File` feature, run the endpoint application via `python endpoint.py`. This will run another Flask application with a WSGI server running on http://localhost:5001. Click `Save to File` and all tasks will be written to a file `file.txt` in the `output` folder.
8. Each task has a `Mark As Complete` button. Clicking it will move the task from incomplete to completed.

## Types of telemetry sent

There are various types of telemetry that are being sent in the sample application. Refer to [Telemetry Type in Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python#telemetry-type-mappings). Every button click hits an endpoint that exists in the flask application, so they will be treated as incoming requests (`requests` table in Azure Monitor). A database call is also made every time a button is clicked, so a dependency type telemetry is sent (`dependency` table in Azure Monitor). Utilizing the `Save to File` feature will make an http call to your local endpoint using the `requests` library, which will generate telemetry (`dependency` table in Azure Monitor).
