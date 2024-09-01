use crate::Data;
use axum::response::IntoResponse;
use axum::{
    extract::{Json, State},
    response::sse::{KeepAlive, Sse},
};
use codegeex4::{
    api::{ChatCompletionRequest, ChatCompletionResponse},
    stream::Streamer,
};
use std::sync::Arc;
use std::time::Duration;
pub enum ChatResponder {
    Streamer(Sse<Streamer>),
    Completion(ChatCompletionResponse),
}

impl IntoResponse for ChatResponder {
    fn into_response(self) -> axum::response::Response {
        match self {
            ChatResponder::Streamer(s) => s.into_response(),
            ChatResponder::Completion(s) => Json(s).into_response(),
        }
    }
}

pub async fn chat(
    State(data): State<Arc<Data>>,
    request: Json<ChatCompletionRequest>,
) -> ChatResponder {
    // debug
    let max_tokens = match request.max_tokens {
        Some(max_tokens) => max_tokens,
        None => 1024,
    };

    let mut prompt = String::new();
    for message in &request.messages {
        prompt.push_str(message.get("content").unwrap());
    }

    if request.stream.is_some_and(|x| x == false) {
        println!("测试链接");
        return ChatResponder::Completion(ChatCompletionResponse {
            id: "".to_string(),
            choices: vec![],
            object: "chat.completion".to_string(),
            created: 0,
            model: "codegeex4".to_string(),
        });
    }

    let (response_tx, rx) = flume::unbounded();

    let _ = tokio::task::spawn_blocking(move || {
        tokio::runtime::Handle::current().block_on(async move {
            data.pipeline
                .lock()
                .unwrap()
                .run(prompt, max_tokens, response_tx.clone()).await;
        });
    });
    println!("打开SSE");
    let streamer = ChatResponder::Streamer(
        Sse::new(Streamer {
            rx,
            status: codegeex4::stream::StreamingStatus::Uninitilized,
        })
        .keep_alive(
            KeepAlive::new()
                .interval(Duration::from_secs(20))
                .text("keep-alive-text"),
        ),
    );

    return streamer;
}
// pub async fn sse() -> Sse<impl Stream<Item = Result<Event,()>>> {
//     let stream =
// }
