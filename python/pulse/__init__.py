"""Pulse Observability Framework - Python SDK.

Unified observability for robotics applications with OpenTelemetry integration.
"""

from .pulse import Pulse, new_pulse, pulse_context
from .options import (
    Environment,
    ServiceOptions, 
    PulseOptions,
    default_pulse_options,
    default_telemetry,
    default_profiling,
    default_foxglove,
)

__version__ = "0.1.0"

__all__ = [
    "Pulse",
    "new_pulse",
    "pulse_context",
    "Environment",
    "ServiceOptions",
    "PulseOptions", 
    "default_pulse_options",
    "default_telemetry",
    "default_profiling", 
    "default_foxglove",
]
