"""Main Pulse observability client."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, List, Optional
import logging as stdlib_logging

from .options import ServiceOptions, PulseOptions, default_pulse_options
from .internal.telemetry import Telemetry
from .internal.logging import Logger
from .internal.metrics import Metrics  
from .internal.tracing import Tracing
from .internal.profiling import Profiler
from .internal.foxglove import UnifiedMcapWriter


class Pulse:
    """Main observability client providing unified access to logging, metrics, tracing, profiling, and MCAP recording.
    
    The Pulse client automatically sets up:
    - Structured logging with OpenTelemetry integration
    - Metrics collection and export  
    - Distributed tracing
    - Continuous profiling (if enabled)
    - MCAP recording for Foxglove Studio (if enabled)
    """
    
    def __init__(
        self,
        service_options: ServiceOptions,
        pulse_options: PulseOptions,
        telemetry: Telemetry,
        logger: Logger,
        metrics: Metrics,
        tracing: Tracing,
        profiler: Optional[Profiler] = None,
        unified_mcap: Optional[UnifiedMcapWriter] = None,
    ) -> None:
        """Initialize Pulse client with all components."""
        # Public interfaces
        self.logger = logger
        self.metrics = metrics  
        self.tracing = tracing
        self.profiler = profiler
        
        # Private components
        self._telemetry = telemetry
        self._unified_mcap = unified_mcap
        self._service_options = service_options
        self._pulse_options = pulse_options
        
    @property
    def telemetry(self) -> Telemetry:
        """Access to unified OpenTelemetry client."""
        return self._telemetry
    
    async def close(self) -> None:
        """Gracefully shut down all Pulse components.
        
        Stops profiling, closes MCAP recording, and shuts down telemetry provider.
        Should be called when application is terminating to ensure data is flushed.
        """
        errors: List[Exception] = []
        
        # Stop profiler first
        if self.profiler:
            try:
                await self.profiler.stop()
            except Exception as e:
                errors.append(Exception(f"Failed to stop profiler: {e}"))
        
        # Close MCAP writer  
        if self._unified_mcap:
            try:
                await self._unified_mcap.close()
            except Exception as e:
                errors.append(Exception(f"Failed to close MCAP writer: {e}"))
        
        # Shutdown telemetry last
        if self._telemetry:
            try:
                await self._telemetry.shutdown()
            except Exception as e:
                errors.append(Exception(f"Failed to shutdown telemetry: {e}"))
                
        if errors:
            # Log all errors but only raise the first one
            for error in errors[1:]:
                stdlib_logging.error(str(error))
            raise errors[0]


async def new_pulse(
    service_options: ServiceOptions, 
    pulse_options: PulseOptions
) -> Pulse:
    """Create a new Pulse observability client.
    
    Example usage:
    
        service_opts = ServiceOptions(
            name="my-service",
            version="1.0.0", 
            environment=Environment.DEVELOPMENT
        )
        
        pulse_opts = default_pulse_options()
        
        async with pulse_context(service_opts, pulse_opts) as pulse:
            pulse.logger.info("Hello, world!")
    """
    # Initialize telemetry first
    telemetry = await Telemetry.new(service_options, pulse_options.telemetry)
    
    # Initialize logging
    logger = await Logger.new(service_options, telemetry)
    
    # Initialize metrics
    metrics = await Metrics.new(service_options, telemetry)
    
    # Initialize tracing  
    tracing = await Tracing.new(service_options, telemetry)
    
    # Initialize profiler if enabled
    profiler = None
    if pulse_options.profiling.enabled:
        profiler = await Profiler.new(service_options, pulse_options.profiling)
    
    # Initialize MCAP writer if enabled
    unified_mcap = None
    if pulse_options.foxglove.enabled:
        unified_mcap = await UnifiedMcapWriter.new(pulse_options.foxglove)
        
    return Pulse(
        service_options=service_options,
        pulse_options=pulse_options,
        telemetry=telemetry,
        logger=logger,
        metrics=metrics,
        tracing=tracing, 
        profiler=profiler,
        unified_mcap=unified_mcap,
    )


@asynccontextmanager
async def pulse_context(
    service_options: ServiceOptions,
    pulse_options: PulseOptions
) -> AsyncIterator[Pulse]:
    """Context manager for Pulse client with automatic cleanup."""
    pulse = await new_pulse(service_options, pulse_options)
    try:
        yield pulse
    finally:
        await pulse.close()
