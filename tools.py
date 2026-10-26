import os
import json
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv(override=True)

# API keys
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

# Send notification
def send_notification(message):
    requests.post(
        pushover_url,
        data={
            "user": pushover_user,
            "token": pushover_token,
            "message": message
        }
    )

# Tool to log user contact
def log_user_contact(email, name="Not provided", notes="Not provided"):
    send_notification(f"Received interedt from email {email} named {name} about {notes}")
    return "OK"

log_user_contact_json = {
    "name": "log_user_contact",
    "description": "Use this tool to record that a user wants to be in contact and has provided an email address.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address provided by the user."},
            "name": {"type":"string", "description": "The name provided by the user."},
            "notes": {"type": "string", "description": "Any other details provided by the user other than email or name."}
        }
    },
    "required": ["email"],
    "additionalParameters": False
}

# Tool to notify for unknown question.
def log_unknown_question(question):
    send_notification(f"Informing you of a question I could not answer: {question}")
    return "OK"

log_unknown_question_json = {
    "name": "log_unknown_question",
    "description": "Always use this tool to record questions that you are not able to answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "Question from the user."}
        }
    },
    "required": ["question"],
    "additionalParameters": False
}

# List of tools available
tools = [
    {"type": "function", "function": log_user_contact_json},
    {"type": "function", "function": log_unknown_question_json},
]

# Map of tools for robust calling
tools_map = {
    "log_user_contact": log_user_contact,
    "log_unknown_question": log_unknown_question,
}

# Handle tools calling
def handle_tool_call(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool = tools_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool " + tool_name
        print(f"Called tool {tool_name} with result {result}", flush=True)
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
            }
        )
    return results