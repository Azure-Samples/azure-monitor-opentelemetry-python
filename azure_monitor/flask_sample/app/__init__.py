import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import Config
from flask_sqlalchemy import SQLAlchemy
from azure_monitor.export.metrics import AzureMonitorMetricsExporter
from azure_monitor.export.trace import AzureMonitorSpanExporter
from opentelemetry import metrics, trace
from opentelemetry.ext.flask import FlaskInstrumentor
from opentelemetry.ext.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.ext.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

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

# Set global MeterProvider before recording
metrics.set_meter_provider(MeterProvider())

metrics_exporter = AzureMonitorMetricsExporter(
    connection_string=Config.CONNECTION_STRING
)

meter = metrics.get_meter("ToDoApp")
metrics.get_meter_provider().start_pipeline(meter, metrics_exporter, 5)

entries_counter = meter.create_metric(
    name="entries",
    description="number of entries",
    unit="1",
    value_type=int,
    metric_type=Counter,
    label_keys=("environment",),
)
testing_labels = {"environment": "testing"}

# Import here to avoid circular imports
from app import routes  # noqa isort:skip

# Processor function for changing the role name of the app
def callback_function(envelope):
    envelope.tags['ai.cloud.role'] = "To-Do App"
    return True

# Adds the telemetry processors
trace_exporter.add_telemetry_processor(callback_function)
metrics_exporter.add_telemetry_processor(callback_function)

app.run(host='localhost', port=5000)
