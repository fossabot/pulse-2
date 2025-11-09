"""Service identity and configuration options."""

from dataclasses import dataclass, field
from typing import Dict

from .environment import Environment


@dataclass
class ServiceOptions:
    """Service identity and configuration.
    
    Defines the core service identity used across all telemetry components.
    """
    
    # Service name (required)
    name: str
    
    # Service version (optional, defaults to "unknown")
    version: str = "unknown"
    
    # Deployment environment
    environment: Environment = Environment.DEVELOPMENT
    
    # Additional service-level attributes for telemetry
    attributes: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate service options after initialization."""
        if not self.name:
            raise ValueError("Service name is required")
        
        if not isinstance(self.environment, Environment):
            raise ValueError(f"Environment must be Environment enum, got {type(self.environment)}")
