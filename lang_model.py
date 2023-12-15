from openai import OpenAI

API_KEY = "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"
GPT3_MODEL = "gpt-3.5-turbo-1106"
COMPLETION_MODEL = "gpt-3.5-turbo-instruct"
client = OpenAI(api_key=API_KEY)


def chat_response(sys_content: str, text_in: str) -> str:
    response = client.chat.completions.create(
        model=GPT3_MODEL,
        messages=[
            {
                "role": "system",
                "content": sys_content,
            },
            {"role": "user", "content": text_in},
        ],
    )
    out = response.choices[0].message.content
    print(f"Response: {out}")
    return out


def completion_response(text_in: str) -> str:
    response = client.completions.create(
        model=COMPLETION_MODEL,
        echo=True,
        max_tokens=1500,
        prompt=text_in,
        n=1,
        # stop=[". ", "? ", "! "],
    )
    response.choices[0].text


def general(text_in: str) -> str:
    print("General Query")
    sys_content = """You are a general use short-form assistant. 
    The user will provide a small amount of text, you must follow the instructions as best as you can as concisely as possible.
    Use as few words as you can that are still gramatically correct. Do not send more than one line of text unless specified.
    If the request is for a specific word or phrase, respond with only the answer, and without punctuation."""
    return chat_response(sys_content, text_in)


def spellcheck(text_in: str) -> str:
    print("Spellcheck Query")
    sys_content = "You are a spellchecking assistant. The user will send text, you must correct any spelling mistakes to the most likely correct word based on the context. You must reply with the exact same text, but with the appropriate corrections. You *must not* change the input in any other way. You *must* only reply with the corrected text. Do not add any other text for any reason."
    return chat_response(sys_content, text_in)


def insert(text_in: str) -> str:
    print("Insert Query")
    ind = "|..|"
    sys_content = f"""You are a insertion short-form assistant.
    The user will provide a small amount of text, you must replace the string "{ind}" with whatever is appropriate, given the context.
    You *must* respond with the *exact same* text, except for the "{ind}" indicator, which you must replace.
    Insert as few words as you can that are still gramatically correct. 
    Only add the answer, do not add additional context.
    """
    examples = f"""Examples: 
    User: as we all know, the effile tower is {ind} feet tall.
    Assistant: as we all know, the effile tower is 1,083 feet tall.

    User: You know what they say. Never put the cart before {ind}
    Assistant: You know what they say. Never put the cart before the horse.

    User: the words {ind} also mean happy
    Assistant: the words joy, cheery, and delight also mean happy
    
    User: Harare is the capital of Zimbabwe, it's best known for its vibrant culture and lively atmosphere. Another lovely city nearby is Bulawayo. Bulawayo's name comes from {ind}
    Assistant: Harare is the capital of Zimbabwe, it's best known for its vibrant culture and lively atmosphere. Another lovely city nearby is Bulawayo. Bulawayo's name comes from the Ndebele words "iBhulu" and "lo," meaning "the place of slaughter."""
    return chat_response(sys_content + examples, text_in)


def complete(text_in: str) -> str:
    print("Completion Query")
    return completion_response(text_in)
