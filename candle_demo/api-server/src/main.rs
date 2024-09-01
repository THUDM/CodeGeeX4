mod args;
mod model;
mod server;
mod streamer;
use axum::{
    http::{self, Method},
    routing, Router,
};
use candle_core as candle;
use candle_core::DType;
use candle_nn::VarBuilder;
use clap::Parser;
use codegeex4::{args::Args, TextGenerationApiServer};
use codegeex4::codegeex4::*;
use codegeex4::TextGeneration;
use hf_hub::{Repo, RepoType};
use owo_colors::{self, OwoColorize};
use rand::Rng;
use server::chat;
use std::sync::{Arc, Mutex};
use tokenizers::Tokenizer;
use tower_http::cors::{AllowOrigin, CorsLayer};

pub struct Data {
    pub pipeline: Mutex<TextGenerationApiServer>,
}

#[tokio::main]
async fn main() {
    let args = args::Args::parse();
     println!(
         "{} Server Binding On {} with {} workers",
         "[INFO]".green(),
         &args.address.purple(),
         &args.workers.purple()
     );

     let mut seed: u64 = 0;
     if let Some(_seed) = args.seed {
         seed = _seed;
     } else {
         let mut rng = rand::thread_rng();
         seed = rng.gen();
     }
     println!("Using Seed {}", seed.red());
     let api = hf_hub::api::sync::ApiBuilder::from_cache(hf_hub::Cache::new(args.cache_path.into()))
         .build()
         .unwrap();

     let model_id = match args.model_id {
         Some(model_id) => model_id.to_string(),
         None => "THUDM/codegeex4-all-9b".to_string(),
     };
     let revision = match args.revision {
         Some(rev) => rev.to_string(),
         None => "main".to_string(),
     };
     let repo = api.repo(Repo::with_revision(model_id, RepoType::Model, revision));
     let tokenizer_filename = match args.tokenizer {
         Some(file) => std::path::PathBuf::from(file),
         None => api
             .model("THUDM/codegeex4-all-9b".to_string())
             .get("tokenizer.json")
             .unwrap(),
     };
     let filenames = match args.weight_file {
         Some(weight_file) => vec![std::path::PathBuf::from(weight_file)],
         None => {
             candle_examples::hub_load_safetensors(&repo, "model.safetensors.index.json").unwrap()
         }
     };
     let tokenizer = Tokenizer::from_file(tokenizer_filename).expect("Tokenizer Error");
     let start = std::time::Instant::now();
     let config = Config::codegeex4();
     let device = candle_examples::device(args.cpu).unwrap();
     let dtype = if device.is_cuda() {
         DType::BF16
     } else {
         DType::F32
     };
     println!("DType is {:?}", dtype.yellow());
     let vb = unsafe { VarBuilder::from_mmaped_safetensors(&filenames, dtype, &device).unwrap() };
     let model = Model::new(&config, vb).unwrap();

     println!("模型加载完毕 {:?}", start.elapsed().as_secs().green());

     let  pipeline = TextGenerationApiServer::new(
         model,
         tokenizer,
         seed,
         args.temperature,
         args.top_p,
         args.repeat_penalty,
         args.repeat_last_n,
         args.verbose_prompt,
         &device,
         dtype,
     );
     let server_data = Arc::new(Data{
	pipeline: Mutex::new(pipeline)
     });
     
    let allow_origin = AllowOrigin::any();
    let allow_methods = tower_http::cors::AllowMethods::any();
    let allow_headers = tower_http::cors::AllowHeaders::any();
    let cors_layer = CorsLayer::new()
        .allow_methods(allow_methods)
        .allow_headers(allow_headers)
        .allow_origin(allow_origin);
    let chat = Router::new()
    // .route("/v1/chat/completions", routing::post(raw))
        .route("/v1/chat/completions", routing::post(chat))
        .layer(cors_layer)
	.with_state(server_data)
	;
    // .with_state(Arc::new(server_data));
    let listener = tokio::net::TcpListener::bind(args.address).await.unwrap();
    axum::serve(listener, chat).await.unwrap();
}
