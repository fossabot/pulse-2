"""Metrics implementation."""

from typing import Any, Dict, Optional
from ..options import ServiceOptions


class Counter:
    """Counter metric - stub implementation."""
    
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
    
    def add(self, value: int, attributes: Optional[Dict[str, str]] = None) -> None:
        """Add to counter."""
        print(f"METRIC: {self.name}+={value} {attributes or ''}")


class Metrics:
    """Metrics client - stub implementation."""
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def new(
        cls,
        service_options: ServiceOptions,
        telemetry: Any
    ) -> "Metrics":
        """Create new metrics instance."""
        return cls()
    
    def create_counter(self, name: str, description: str) -> Counter:
        """Create counter metric."""
        return Counter(name, description)
    
    async def close(self) -> None:
        """Close metrics."""
        pass
