"""Foxglove/MCAP implementation."""

from typing import Any
from ..options import FoxgloveOptions


class UnifiedMcapWriter:
    """MCAP writer for Foxglove Studio - stub implementation."""
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def new(cls, foxglove_options: FoxgloveOptions) -> "UnifiedMcapWriter":
        """Create new MCAP writer instance."""
        return cls()
    
    async def close(self) -> None:
        """Close MCAP writer."""
        print("MCAP: Writer closed")
