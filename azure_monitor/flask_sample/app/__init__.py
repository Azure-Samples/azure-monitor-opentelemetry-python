import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import Config
from flask_sqlalchemy import SQLAlchemy

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Set global TracerProvider before instrumenting
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "flask-sample"})
    )
)

# Enable tracing for sqlalchemy library
SQLAlchemyInstrumentor().instrument()

# Enable tracing for Flask library
FlaskInstrumentor().instrument_app(app)

# Enable tracing for requests library
RequestsInstrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter(
    connection_string=Config.CONNECTION_STRING
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(trace_exporter)
)

# Import here to avoid circular imports
from app import routes  # noqa isort:skip

app.run(host='localhost', port=5000)
