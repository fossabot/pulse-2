"""Environment configuration types."""

from enum import Enum

class Environment(Enum):
    """Deployment environment types."""
    
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    JETSON = "jetson"  # Embedded robotics systems
    
    def __str__(self) -> str:
        return self.value
