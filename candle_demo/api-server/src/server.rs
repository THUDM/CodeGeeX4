use crate::args::Args;
use actix_web::{web, App, HttpResponse, HttpServer};
use owo_colors::OwoColorize;

#[derive(Debug)]
pub struct Server {
    config: Args,
}

impl Server {
    pub fn new(config: Args) -> Self {
        return Server { config };
    }
    pub async fn run(&self) -> () {
        HttpServer::new(move || App::new())
            .bind(&self.config.address)
            .expect(&format!("{}", "Unable To Bind Server !".red()))
            .workers(self.config.workers)
            .run()
            .await
            .expect(&format!("{}", "Unable To Run the Server !".red()));
    }
}

// use super::api::*;
// use uuid;
// pub async fn chat(request: ChatCompletionRequest) ->impl Responder {
//     if request.stream == true {
// 	return Htt
//     }
// }
