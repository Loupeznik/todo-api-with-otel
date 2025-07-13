import logging

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import \
    OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import \
    OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.config import settings


def setup_instrumentation():
    """
    Sets up logging and OpenTelemetry tracing for the application.
    """
    resource = Resource.create(attributes={
        SERVICE_NAME: "todo-api-with-otel"
    })

    if settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        print(
            f"Setting up OpenTelemetry exporter for endpoint: {settings.OTEL_EXPORTER_OTLP_ENDPOINT}")

        tracer_provider = TracerProvider(resource=resource)
        span_exporter = OTLPSpanExporter(
            endpoint=f"{settings.OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces",
            headers={}
        )
        processor = BatchSpanProcessor(span_exporter)
        tracer_provider.add_span_processor(processor)
        trace.set_tracer_provider(tracer_provider)

        metric_exporter = OTLPMetricExporter(
            endpoint=f"{settings.OTEL_EXPORTER_OTLP_ENDPOINT}/v1/metrics",
            headers={}
        )
        reader = PeriodicExportingMetricReader(
            metric_exporter,
            export_interval_millis=5000
        )
        meter_provider = MeterProvider(
            resource=resource, metric_readers=[reader])
        metrics.set_meter_provider(meter_provider)

        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Configure basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[]
        )

        # Set up OpenTelemetry logging
        logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(logger_provider)

        log_exporter = OTLPLogExporter(
            endpoint=f"{settings.OTEL_EXPORTER_OTLP_ENDPOINT}/v1/logs",
            headers={}
        )

        log_processor = BatchLogRecordProcessor(
            log_exporter,
            max_queue_size=2048,
            export_timeout_millis=30000,
            max_export_batch_size=512,
        )
        logger_provider.add_log_record_processor(log_processor)

        otlp_handler = LoggingHandler(
            level=logging.INFO,
            logger_provider=logger_provider
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        root_logger.addHandler(otlp_handler)
        root_logger.addHandler(console_handler)
        root_logger.setLevel(logging.INFO)

        logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
        logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
        logging.getLogger("uvicorn.access").setLevel(logging.WARN)
        logging.getLogger("fastapi").setLevel(logging.WARN)

        # Auto-instrument libraries
        SQLAlchemyInstrumentor().instrument()
        Psycopg2Instrumentor().instrument()

        LoggingInstrumentor().instrument(set_logging_format=False)

        print("OpenTelemetry instrumentation setup complete")
    else:
        print(
            "OpenTelemetry exporter endpoint not configured. Traces will not be exported.")
