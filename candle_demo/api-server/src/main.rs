mod api;
mod args;
mod server;
mod model;
use clap::Parser;
use owo_colors::OwoColorize;

#[tokio::main]
async fn main() {
    let args = args::Args::parse();
    let server = server::Server::new(args.clone());
    println!(
        "{} Server Binding On {} with {} workers",
        "[INFO]".green(),
        &args.address.purple(),
        &args.workers.purple()
    );
    server.run().await;
}
