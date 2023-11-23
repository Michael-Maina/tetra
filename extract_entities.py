import openai
import os
from flask import jsonify
import re


openai.api_key = os.getenv("OPENAI_API_KEY")

labels = ["person", "email", "phone_number", "date", "time"]
client = openai.OpenAI()

def system_message(labels):
    return f"""
You are an expert in Natural Language Processing designed to output JSON .
Your task is to identify entities related to meeting setup that would be used to create an event instance in the Google Calendar API.
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
        "date": ["23rd January 2023"],
        "time": ["3 PM"]
    }
--"""

def extract_entities(text):
    messages = [
        {"role": "system", "content": system_message(labels)},
        {"role": "assistant", "content": assistant_message()},
        {"role": "user", "content": user_message(text=text)}
    ]
    response = client.chat.completions.create( #openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=messages,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return extract_content(str(response))


def extract_content(api_output):
    # Find the start and end of the content string
    start_index = api_output.find("content='{") + len("content='{")
    end_index = api_output.find("}'", start_index)

    # Extract and clean the content string
    content_str = api_output[start_index:end_index]
    content_str = content_str.replace('\\n', '').replace('\\', '')  # Remove newlines and backslashes

    # Initialize a dictionary
    content_dict = {}

    # Split the string into key-value pairs
    pairs = content_str.split('", "')
    split_pairs = pairs[0].split(',')

    for pair in split_pairs:
        pair = pair.strip()
        pair = pair.split(':')
        key = re.findall(r'"(.*?)"', pair[0])
        value = re.findall(r'"(.*?)"', pair[1])
        content_dict[key[0]] = value[0]

    return content_dict
