use crate::Options;
use opentelemetry::KeyValue;
use opentelemetry_sdk::Resource;
use opentelemetry_semantic_conventions::{
    resource::{SERVICE_NAME, SERVICE_VERSION},
    SCHEMA_URL,
};

#[cfg_attr(
    not(all(feature = "logs", feature = "trace")),
    allow(unused_variables, dead_code)
)]
pub(crate) fn get_resource(options: &Options) -> Resource {
    Resource::from_schema_url(
        vec![
            KeyValue::new(SERVICE_NAME, options.service_name.clone()),
            KeyValue::new(SERVICE_VERSION, options.service_version.clone()),
        ],
        SCHEMA_URL,
    )
}
