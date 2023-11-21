import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

labels = ["person", "email", "phone_number", "date", "time"]

def system_message(labels):
    return f"""
You are an expert in Natural Language Processing designed to output JSON . Your task is to identify entities related to meeting setup in a given text.
The possible entity types for this task are: ({", ".join(labels)})."""

def user_message(text):
    return f"""
TASK:
    text: {text}
"""
def assistant_message():
    return """
EXAMPLE:
    Text: 'Hey there, can you set up a meeting for me with Jane Smith?
    Her email is jane.smith@domain.com and her phone number is 555-678-9012.
    How about next Thursday at 3 PM? Thanks!'
    {
        "person": ["Jane Smith"],
        "email": ["jane.smith@domain.com"],
        "phone_number": ["555-678-9012"],
        "date": ["next Thursday"],
        "time": ["3 PM"]
    }
--"""

def extract_entities(text):
    messages = [
        {"role": "system", "content": system_message(labels)},
        {"role": "assistant", "content": assistant_message()},
        {"role": "user", "content": user_message(text=text)}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        response_format={ "type": "json_object" },
        messages=messages,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message["content"]
