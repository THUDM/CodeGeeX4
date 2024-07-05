"""
References: https://github.com/leptonai/search_with_lepton
"""
import gradio as gr

from backend.services.chat import chat

if __name__ == "__main__":
    demo = gr.ChatInterface(chat).queue()
    demo.launch(server_name="127.0.0.1", server_port=8080)
