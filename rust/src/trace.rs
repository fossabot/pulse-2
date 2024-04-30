use crate::{Options, Result};
use opentelemetry_otlp::WithExportConfig;
use opentelemetry_sdk::{
    runtime,
    trace::{BatchConfigBuilder, RandomIdGenerator, Tracer},
};
use std::time::Duration;

pub use tracing::{
    debug, debug_span, error, error_span, info, info_span, instrument, span, trace, trace_span,
    warn, warn_span,
};

pub(crate) fn layer(options: &Options) -> Result<Tracer> {
    let pipeline = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_trace_config(
            opentelemetry_sdk::trace::Config::default()
                .with_id_generator(RandomIdGenerator::default())
                .with_resource(crate::common::get_resource(options)),
        )
        .with_batch_config(
            BatchConfigBuilder::default()
                .with_scheduled_delay(Duration::from_millis(1000))
                .build(),
        );

    let pipeline = match options.network.advanced_opts.connection_type {
        crate::ConnectionType::Grpc => pipeline.with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint(options.network.uri()),
        ),
        crate::ConnectionType::Http => pipeline.with_exporter(
            opentelemetry_otlp::new_exporter()
                .http()
                .with_endpoint(options.network.uri()),
        ),
    };

    Ok(pipeline.install_batch(runtime::Tokio)?)
}
