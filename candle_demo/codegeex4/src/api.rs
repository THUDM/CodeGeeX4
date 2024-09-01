use std::collections::HashMap;

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatCompletionChunk {
    pub id: String,
    pub object: String,
    pub created: u64,
    pub model: String,
    pub choices: Vec<ChatChoiceStream>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Choice {
    pub delta: ChatChoiceData,
    pub finish_reason: Option<String>,
    pub index: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatCompletionRequest {
    pub messages: Vec<HashMap<String, String>>,
    pub model: String,
    #[serde(default)]
    pub stream: Option<bool>, //false
    pub temperature: Option<f32>, //0.7
    #[serde(default)]
    pub top_p: Option<f32>, //1.0
    #[serde(default)]
    pub max_tokens: Option<usize>, //None
    #[serde(default)]
    pub stop: Option<String>,
    #[serde(default)]
    presence_penalty: Option<f32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatCompletionResponse {
    pub id: String,
    pub choices: Vec<ChatChoice>,
    pub created: u64,
    pub model: String,
    pub object: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatCompletionResponseStream {
    pub id: String,
    pub choices: Vec<ChatChoiceStream>,
    pub created: u64,
    pub model: String,
    pub object: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatChoice {
    pub index: usize,
    pub message: ChatChoiceData,
    pub finish_reason: Option<String>,
    pub logprobs: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatChoiceStream {
    pub index: usize,
    pub delta: ChatChoiceData,
    pub finish_reason: Option<String>,
    pub logprobs: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatChoiceData {
    pub role: String,
    pub content: Option<String>,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatCompletionUsageResponse {
    pub request_id: String,
    pub created: u64,
    pub completion_tokens: usize,
    pub prompt_tokens: usize,
    pub total_tokens: usize,
    pub prompt_time_costs: usize,
    pub completion_time_costs: usize,
}
