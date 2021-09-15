import requests

from opentelemetry import trace

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Set global TracerProvider before instrumenting
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "http-sample-A"})
    )
)

# Enable tracing for requests library
RequestsInstrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter()
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(trace_exporter)
)
tracer = trace.get_tracer(__name__)

# Call django app
response = requests.get("http://127.0.0.1:8000/projects", timeout=5)
