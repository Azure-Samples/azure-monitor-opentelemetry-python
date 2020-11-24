import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import Config
from flask_sqlalchemy import SQLAlchemy
from microsoft.opentelemetry.exporter.azuremonitor import AzureMonitorSpanExporter
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
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

# Import here to avoid circular imports
from app import routes  # noqa isort:skip

# Processor function for changing the role name of the app
def callback_function(envelope):
    envelope.tags['ai.cloud.role'] = "To-Do App"
    return True

# Adds the telemetry processors
trace_exporter.add_telemetry_processor(callback_function)

app.run(host='localhost', port=5000)
