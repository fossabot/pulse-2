use crate::{Options, Result};
use env_logger::fmt::{
    style::{AnsiColor, Style},
    Formatter,
};
use log::Record;
use opentelemetry_appender_log::OpenTelemetryLogBridge;
use opentelemetry_otlp::WithExportConfig;
use opentelemetry_sdk::logs::LoggerProvider;
use opentelemetry_sdk::runtime;
use std::io::Write;

pub use log::{debug, error, info, trace, warn};

pub(crate) struct Logger {
    otel_logger: Box<dyn log::Log>,
    std_logger: Box<dyn log::Log>,
}

impl Logger {
    pub fn new(options: &Options) -> Result<Self> {
        let config = opentelemetry_sdk::logs::Config::default()
            .with_resource(crate::common::get_resource(options));

        let provider = match options.network.advanced_opts.connection_type {
            crate::ConnectionType::Grpc => LoggerProvider::builder()
                .with_config(config)
                .with_batch_exporter(
                    opentelemetry_otlp::new_exporter()
                        .tonic()
                        .with_endpoint(options.network.uri())
                        .build_log_exporter()?,
                    runtime::Tokio,
                )
                .build(),
            crate::ConnectionType::Http => LoggerProvider::builder()
                .with_config(config)
                .with_batch_exporter(
                    opentelemetry_otlp::new_exporter()
                        .http()
                        .with_endpoint(options.network.uri())
                        .build_log_exporter()?,
                    runtime::Tokio,
                )
                .build(),
        };

        let l: log::Level = options.log_level.into();
        let styler = Styler::new(&options.service_name);
        let std_logger = env_logger::Builder::new()
            .filter_level(l.to_level_filter())
            .format(move |buf, record| styler.format(buf, record))
            .build();

        Ok(Self {
            otel_logger: Box::new(OpenTelemetryLogBridge::new(&provider)),
            std_logger: Box::new(std_logger),
        })
    }
}

impl log::Log for Logger {
    fn enabled(&self, metadata: &log::Metadata) -> bool {
        self.otel_logger.enabled(metadata)
    }

    fn log(&self, record: &log::Record) {
        self.std_logger.log(record);
        self.otel_logger.log(record);
    }

    fn flush(&self) {
        self.std_logger.flush();
        self.otel_logger.flush();
    }
}

struct Styler {
    service_name: String,
    timestamp_style: Style,
    service_name_style: Style,
    error_style: Style,
    warn_style: Style,
    info_style: Style,
    debug_style: Style,
    trace_style: Style,
}

impl Styler {
    pub fn new(service_name: impl Into<String>) -> Self {
        Self {
            service_name: service_name.into(),
            timestamp_style: Style::new()
                .fg_color(Some(AnsiColor::Black.into()))
                .italic(),
            service_name_style: Style::new().fg_color(Some(AnsiColor::Black.into())).bold(),
            error_style: Style::new().fg_color(Some(AnsiColor::Red.into())),
            warn_style: Style::new().fg_color(Some(AnsiColor::Yellow.into())),
            info_style: Style::new().fg_color(Some(AnsiColor::Green.into())),
            debug_style: Style::new().fg_color(Some(AnsiColor::Blue.into())),
            trace_style: Style::new().fg_color(Some(AnsiColor::BrightWhite.into())),
        }
    }

    pub fn format(
        &self,
        buf: &mut Formatter,
        record: &Record,
    ) -> std::result::Result<(), std::io::Error> {
        let timestamp_style = &self.timestamp_style;
        let level_style = match record.level() {
            log::Level::Error => &self.error_style,
            log::Level::Warn => &self.warn_style,
            log::Level::Info => &self.info_style,
            log::Level::Debug => &self.debug_style,
            log::Level::Trace => &self.trace_style,
        };
        let service_name_style = &self.service_name_style;

        let file = match record.file() {
            Some(p) => format!("[{p}]"),
            None => "".to_owned(),
        };

        writeln!(
            buf,
            "{timestamp_style}{}{timestamp_style:#} [{level_style}{}{level_style:#}:{service_name_style}{}{service_name_style:#}] {} {}",
            buf.timestamp(),
            record.level(),
            &self.service_name,
            file,
            record.args(),
        )
    }
}
