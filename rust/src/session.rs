use crate::{Options, Result};
use opentelemetry_sdk::trace::Tracer;
use tracing::Subscriber;
use tracing_opentelemetry::OpenTelemetryLayer;
use tracing_subscriber::{layer::SubscriberExt, registry::LookupSpan, util::SubscriberInitExt};

pub struct Session;

impl Drop for Session {
    fn drop(&mut self) {
        opentelemetry::global::shutdown_tracer_provider();
    }
}

pub fn init() -> Result<Session> {
    init_impl(Options::from_default()?)
}

pub fn init_with_options(options: Options) -> Result<Session> {
    init_impl(Options::merge_with(options)?)
}

fn init_impl(options: Options) -> Result<Session> {
    tracing_subscriber::registry()
        .with(tracing_subscriber::filter::LevelFilter::from_level(
            options.log_level.into(),
        ))
        .with(tracing_layer(&options)?)
        .init();

    #[cfg(feature = "logs")]
    {
        if let Ok(Some(logger)) = logger(&options) {
            log::set_boxed_logger(logger)?;
        }
        let l: log::Level = options.log_level.into();
        log::set_max_level(l.to_level_filter());
    }

    Ok(Session)
}

#[cfg_attr(not(feature = "trace"), allow(unused_variables, dead_code))]
fn tracing_layer<'a, S>(options: &Options) -> Result<Option<OpenTelemetryLayer<S, Tracer>>>
where
    S: Subscriber + for<'span> LookupSpan<'span>,
{
    #[cfg(feature = "trace")]
    {
        let tracer = crate::trace::layer(options)?;
        Ok(Some(OpenTelemetryLayer::new(tracer)))
    }

    #[cfg(not(feature = "trace"))]
    {
        Ok(None)
    }
}

#[cfg_attr(not(feature = "logs"), allow(unused_variables, dead_code))]
fn logger(options: &Options) -> Result<Option<Box<dyn log::Log>>> {
    #[cfg(feature = "logs")]
    {
        Ok(Some(Box::new(crate::log::Logger::new(options)?)))
    }

    #[cfg(not(feature = "logs"))]
    {
        Ok(None)
    }
}
