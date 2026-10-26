import os
from dotenv import load_dotenv
from context import CONTEXT_PROMPT
from openai import OpenAI
from tools import tools, handle_tool_call
import gradio as gr

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

system = [{"role": "system", "content": CONTEXT_PROMPT}]

openai = OpenAI()

def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        msg = response.choices[0].message
        tool_calls = msg.tool_calls
        results = handle_tool_call(tool_calls)
        messages.append(msg)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        title="Digital Resume",
        description="Talk to my AI about my career",
        chatbot=gr.Chatbot(show_label=False)
    ).launch()