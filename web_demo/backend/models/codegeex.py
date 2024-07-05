import torch
from transformers import AutoTokenizer, AutoModel

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name_or_path = "THUDM/codegeex4-all-9b"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name_or_path,
    trust_remote_code=True
).to(device).eval()
