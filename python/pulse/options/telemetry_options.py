"""OpenTelemetry configuration options."""

from dataclasses import dataclass

from .otlp_options import OTLPOptions, default_otlp


@dataclass
class TelemetryOptions:
    """OpenTelemetry export configuration."""
    
    # OTLP export configuration
    otlp: OTLPOptions
    
    # Feature toggles
    enable_logging: bool = True
    enable_metrics: bool = True  
    enable_tracing: bool = True


def default_telemetry() -> TelemetryOptions:
    """Create TelemetryOptions with sensible defaults."""
    return TelemetryOptions(
        otlp=default_otlp(),
        enable_logging=True,
        enable_metrics=True,
        enable_tracing=True,
    )
