from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, MeterProvider

# Set global MeterProvider before recording
metrics.set_meter_provider(MeterProvider())

meter = metrics.get_meter("ToDoApp")
entries_counter = meter.create_metric(
    name="entries",
    description="number of entries",
    unit="1",
    value_type=int,
    metric_type=Counter,
    label_keys=("environment",),
)
testing_labels = {"environment": "testing"}
