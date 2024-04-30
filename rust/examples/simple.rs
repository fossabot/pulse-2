use std::time::Duration;

#[tokio::main]
async fn main() {
    let _session = pulse::init().unwrap();

    pulse::log::info!("this is an info log");
    let mut i: i32 = 0;
    loop {
        i += 1;
        foo(i).await;
        tokio::time::sleep(Duration::from_millis(1000)).await;
    }
}

#[pulse::trace::instrument]
async fn foo(i: i32) {
    pulse::trace::error!("starting function");
    pulse::trace::info!(i = i);

    pulse::log::error!("this is an error log");
    pulse::log::trace!("this is a trace log");
    pulse::log::info!("this is an info log");
    pulse::log::warn!("this is a warn log");
    pulse::log::debug!("this is a debug log");
}
