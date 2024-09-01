use std::time::Duration;
use axum::response::IntoResponse;
use codegeex4::stream::ChatResponse;
use codegeex4::{
    api::{
        ChatChoice, ChatChoiceData, ChatChoiceStream, ChatCompletionRequest,
        ChatCompletionResponse, ChatCompletionResponseStream, ChatCompletionUsageResponse, ChatCompletionChunk,
    },
    stream::{Streamer, self},
};
use axum::{
    body::HttpBody,
    extract::{Json, RawQuery, State},
    response::sse::{Event, KeepAlive, Sse},
    response::Response,
};
use rand;
use std::sync::Arc;
use crate::Data;
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
// pub async fn chat(
// //    State(data): State<Arc<Data>>,
//     request: Json<ChatCompletionRequest>,
// ) -> Json<ChatCompletionResponse> {
//     let us =  ChatCompletionUsageResponse { request_id: "1".to_string(), created: 123, completion_tokens: 123, prompt_tokens: 123, total_tokens:  123, prompt_time_costs:123 , completion_time_costs:123 };
//     let response = ChatCompletionResponse {
// 	id: "codegeex4".to_string(),
// 	choices: vec!(),
// 	created: 0,
// 	model: "123".to_string(),
// 	object: "1",
// 	usage: us,
//     };
//     return Json(response.into());

// }

pub async fn chat(
    State(data): State<Arc<Data>>,
    request: Json<ChatCompletionRequest>,
) -> ChatResponder {
    // debug

    let uuid = uuid::Uuid::new_v4();
    let completion_id = format!("chatcmpl-{}", uuid);
    
    let choice_data = ChatChoiceData {
	role: "assistant".to_string(),
        content: Some("\n\nhi123".to_string()),
    };
    let choice = ChatChoiceStream {
        delta: choice_data.clone(),
        //finish_reason: Some("stop".to_string()),
	finish_reason: None,
        index: 0,
	logprobs: None,
    };
    let choice_not_stream = ChatChoice {
        message: choice_data,
        // finish_reason: Some("stop".to_string()),
	finish_reason: None,
        index: 1,
	logprobs: None,
    };
    let mut prompt = String::new();
    for message in &request.messages {
        prompt.push_str(message.get("content").unwrap());
    }
    println!("request is {:?}", request);
    println!("prompt is {}", prompt);
    println!("uuid {completion_id}");
    
    if request.stream.is_some_and(|x| x==false) {
	println!("测试链接");
	return ChatResponder::Completion(ChatCompletionResponse{
	    id: completion_id.clone(),
        choices: vec![choice_not_stream.clone()],
        object: "chat.completion".to_string(),
        created: 0,
        model: "codegeex4".to_string(),
	});
    }
    
    let (response_tx, rx) = flume::unbounded();
    
    println!("打开SSE");
    let _ = tokio::task::spawn_blocking(move || {
        tokio::runtime::Handle::current().block_on(async move {
	    data.pipeline.lock().unwrap().run(prompt,1024,response_tx.clone());
	});});
    let  streamer = ChatResponder::Streamer(Sse::new(Streamer {
            rx,
            status: codegeex4::stream::StreamingStatus::Uninitilized,
        })
        .keep_alive(
                KeepAlive::new()
                    .interval(Duration::from_millis(
                            100
                    ))
                    .text("keep-alive-text"),
        )
    );
    
    
    return streamer;
}
// pub async fn sse() -> Sse<impl Stream<Item = Result<Event,()>>> {
//     let stream =
// }
