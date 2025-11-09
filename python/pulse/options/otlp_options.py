"""OTLP export configuration."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OTLPOptions:
    """OTLP export configuration."""
    
    # gRPC endpoint (default: localhost:4317)
    grpc_endpoint: str = "http://localhost:4317"
    
    # HTTP endpoint (default: localhost:4318) 
    http_endpoint: str = "http://localhost:4318"
    
    # Use gRPC instead of HTTP
    use_grpc: bool = True
    
    # Optional headers for authentication
    headers: Optional[dict] = None
    
    # Connection timeout in seconds
    timeout: int = 10


def default_otlp() -> OTLPOptions:
    """Create OTLPOptions with sensible defaults."""
    return OTLPOptions(
        grpc_endpoint="http://localhost:4317",
        http_endpoint="http://localhost:4318", 
        use_grpc=True,
        headers=None,
        timeout=10,
    )
