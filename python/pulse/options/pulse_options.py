"""Main Pulse configuration options."""

from dataclasses import dataclass

from .telemetry_options import TelemetryOptions, default_telemetry
from .profiling_options import ProfilingOptions, default_profiling  
from .foxglove_options import FoxgloveOptions, default_foxglove


@dataclass
class PulseOptions:
    """Configuration for Pulse observability client."""
    
    # OpenTelemetry configuration
    telemetry: TelemetryOptions
    
    # Profiling configuration
    profiling: ProfilingOptions
    
    # MCAP/Foxglove configuration
    foxglove: FoxgloveOptions


def default_pulse_options() -> PulseOptions:
    """Create PulseOptions with sensible defaults."""
    return PulseOptions(
        telemetry=default_telemetry(),
        profiling=default_profiling(),
        foxglove=default_foxglove(),
    )
