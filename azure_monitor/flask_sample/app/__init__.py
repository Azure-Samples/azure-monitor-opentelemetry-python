import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from app.metric import meter
from config import Config
from flask_sqlalchemy import SQLAlchemy
from azure_monitor.export.metrics import AzureMonitorMetricsExporter
from azure_monitor.export.trace import AzureMonitorSpanExporter
from opentelemetry import metrics, trace
from opentelemetry.ext.flask import FlaskInstrumentor
from opentelemetry.ext.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.ext.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics.export.controller import PushController
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

trace_exporter = AzureMonitorSpanExporter(
    connection_string=Config.CONNECTION_STRING
)
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(trace_exporter)
)

metrics_exporter = AzureMonitorMetricsExporter(
    connection_string=Config.CONNECTION_STRING
)
PushController(meter, metrics_exporter, 10)

# Processor function for changing the role name of the app
def callback_function(envelope):
    envelope.tags['ai.cloud.role'] = "To-Do App"
    return True

# Adds the telemetry processors
trace_exporter.add_telemetry_processor(callback_function)
metrics_exporter.add_telemetry_processor(callback_function)

app.run(host='localhost', port=5000)
