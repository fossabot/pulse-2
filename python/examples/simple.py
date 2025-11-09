"""Basic Pulse usage example."""

import asyncio
from pulse import ServiceOptions, Environment, default_pulse_options, pulse_context


async def main():
    """Run basic Pulse example."""
    # Configure service identity
    service_opts = ServiceOptions(
        name="example-service",
        version="1.0.0",
        environment=Environment.DEVELOPMENT,
        attributes={"team": "robotics", "component": "navigation"}
    )

    # Use default options
    pulse_opts = default_pulse_options()

    # Use context manager for automatic cleanup
    async with pulse_context(service_opts, pulse_opts) as pulse_client:

        # Structured logging
        pulse_client.logger.info("Service started", extra={"user_id": "123"})

        # Metrics
        counter = pulse_client.metrics.create_counter("requests_total", "Total HTTP requests")
        counter.add(1, {"endpoint": "/api/health"})

        # Tracing
        with pulse_client.tracing.start_span("process_request") as span:
            span.set_attribute("request.id", "req-123")
            pulse_client.logger.info("Processing request", extra={"request_id": "req-123"})

            # Simulate work
            await asyncio.sleep(0.1)

        pulse_client.logger.info("Service stopping")


if __name__ == "__main__":
    asyncio.run(main())
