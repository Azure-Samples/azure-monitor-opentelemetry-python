import psycopg2

from opentelemetry import trace

from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Set global TracerProvider before instrumenting
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "db-sample"})
    )
)

# Enable tracing for psycopg2 library
Psycopg2Instrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter()
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(trace_exporter)
)

cnx = psycopg2.connect(database='test', user='postgres', password='password')
cursor = cnx.cursor()
cursor.execute("CREATE TABLE test (testField integer);")
cursor.execute("INSERT INTO test (testField) VALUES (123)")
cursor.close()
cnx.close()
