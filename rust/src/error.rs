use log::SetLoggerError;
use opentelemetry::{logs::LogError, trace::TraceError};

pub type Result<T> = std::result::Result<T, Error>;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("error loading options: {0}")]
    ConfigurationError(#[from] figment::Error),

    #[error("{0}")]
    OtlpTracerError(#[from] TraceError),

    #[error("{0}")]
    OtlpLogError(#[from] LogError),

    #[error("{0}")]
    SetLoggerError(#[from] SetLoggerError),
}
