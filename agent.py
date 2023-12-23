from openai import OpenAI
from config_handler import config

client = OpenAI(api_key=config["OpenAI"]["OPEN_AI_API_KEY"])
model = "gpt-4-1106-preview"

tools = [
    {
        "type": "function",
        "function": {
            "name": "getName",
            "description": "Get the name of the current chatting user.",
            "parameters": {},
        },
    }
]


def agent():
    assistant = client.beta.assistants.create(
        name="Level 1 Agent",
        instructions="You are an LLM agent. You search the web according to instructions.",
        model=model,
        tools=tools,
    )
    assistant


if __name__ == "__main__":
    agent()
