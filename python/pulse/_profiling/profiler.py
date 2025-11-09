"""Profiling implementation."""

from ...options import ServiceOptions, ProfilingOptions


class Profiler:
    """Profiler client - stub implementation."""
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def new(
        cls,
        service_options: ServiceOptions,
        profiling_options: ProfilingOptions
    ) -> "Profiler":
        """Create new profiler instance."""
        return cls()
    
    async def stop(self) -> None:
        """Stop profiler."""
        print("PROFILER: Stopped")
    
    async def close(self) -> None:
        """Close profiler."""
        pass
