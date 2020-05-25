import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import Config
from flask_sqlalchemy import SQLAlchemy
from azure_monitor.export.trace import AzureMonitorSpanExporter
from azure_monitor.export.metrics import AzureMonitorMetricsExporter
from opentelemetry import trace
from opentelemetry.ext.flask import FlaskInstrumentor
from opentelemetry.ext.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.ext.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Import here to avoid circular imports
from app import routes  # noqa isort:skip

# Set global TracerProvider before instrumenting
trace.set_tracer_provider(TracerProvider())

# Enable tracing for sqlalchemy library
SQLAlchemyInstrumentor().instrument()

# Enable tracing for Flask library
FlaskInstrumentor().instrument_app(app)

# Enable tracing for requests library
RequestsInstrumentor().instrument()

exporter = AzureMonitorSpanExporter()
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(exporter)
)

# Processor function for changing the role name of the app
def callback_function(envelope):
    envelope.tags['ai.cloud.role'] = "To-Do App"
    return True

# Adds the telemetry processor to the trace exporter
exporter.add_telemetry_processor(callback_function)

app.run(host='localhost', port=5000)
