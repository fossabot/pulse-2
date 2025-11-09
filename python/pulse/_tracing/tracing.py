"""Tracing implementation."""

from typing import Any, Generator
from contextlib import contextmanager
from ...options import ServiceOptions


class Span:
    """Span - stub implementation."""
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def set_attribute(self, key: str, value: str) -> None:
        """Set span attribute."""
        print(f"SPAN: {self.name} - {key}={value}")
    
    def __enter__(self):
        print(f"SPAN: Starting {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"SPAN: Ending {self.name}")


class Tracing:
    """Tracing client - stub implementation."""
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def new(
        cls,
        service_options: ServiceOptions,
        telemetry: Any
    ) -> "Tracing":
        """Create new tracing instance."""
        return cls()
    
    @contextmanager
    def start_span(self, name: str) -> Generator[Span, None, None]:
        """Start a new span."""
        span = Span(name)
        try:
            yield span
        finally:
            pass
    
    async def close(self) -> None:
        """Close tracing."""
        pass
