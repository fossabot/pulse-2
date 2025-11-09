"""Foxglove/MCAP configuration options."""

from dataclasses import dataclass
from enum import Enum


class CompressionType(Enum):
    """MCAP compression types."""
    NONE = "none"
    LZ4 = "lz4" 
    ZSTD = "zstd"


@dataclass
class FoxgloveOptions:
    """MCAP recording configuration for Foxglove Studio."""
    
    # Enable MCAP recording
    enabled: bool = False
    
    # MCAP file path
    mcap_path: str = ""
    
    # Chunk size in bytes
    chunk_size: int = 1024 * 1024  # 1MB
    
    # Compression type
    compression: CompressionType = CompressionType.NONE


def default_foxglove() -> FoxgloveOptions:
    """Create FoxgloveOptions with sensible defaults."""
    return FoxgloveOptions(
        enabled=False,
        mcap_path="",
        chunk_size=1024 * 1024,
        compression=CompressionType.NONE,
    )
