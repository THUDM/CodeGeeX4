use clap::Parser;

#[derive(Parser, Debug, Clone)]
#[clap(version, about)]
pub struct Args {
    #[arg(name = "listen", short, long, default_value = "0.0.0.0:3000")]
    pub address: String,
    #[arg(short, long, default_value_t = 1)]
    pub workers: usize,
}
