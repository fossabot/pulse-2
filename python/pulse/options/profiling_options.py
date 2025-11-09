"""Profiling configuration options."""

from dataclasses import dataclass


@dataclass
class ProfilingOptions:
    """Pyroscope profiling configuration."""
    
    # Enable profiling
    enabled: bool = False
    
    # Pyroscope server URL
    server_url: str = "http://localhost:4040"
    
    # Application name for profiling
    application_name: str = ""
    
    # Sample rate (0.0 to 1.0)
    sample_rate: float = 0.01


def default_profiling() -> ProfilingOptions:
    """Create ProfilingOptions with sensible defaults."""
    return ProfilingOptions(
        enabled=False,
        server_url="http://localhost:4040", 
        application_name="",
        sample_rate=0.01,
    )
