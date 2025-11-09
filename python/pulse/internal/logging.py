"""Logger implementation."""

from typing import Any, Optional
from ..options import ServiceOptions


class Logger:
    """Logger client - stub implementation."""
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def new(
        cls,
        service_options: ServiceOptions,
        telemetry: Any
    ) -> "Logger":
        """Create new logger instance."""
        return cls()
    
    def info(self, message: str, extra: Optional[dict] = None) -> None:
        """Log info message."""
        print(f"INFO: {message} {extra or ''}")
    
    def error(self, message: str, extra: Optional[dict] = None) -> None:
        """Log error message."""
        print(f"ERROR: {message} {extra or ''}")
    
    def warn(self, message: str, extra: Optional[dict] = None) -> None:
        """Log warning message."""
        print(f"WARN: {message} {extra or ''}")
    
    async def close(self) -> None:
        """Close logger."""
        pass
