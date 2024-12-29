import pandas as pd
import json
import re

def decode_utf8(str):
    # regex to find utf-8 sequences
    pattern = re.compile(r"(\\u[0-9a-fA-F]{4})+")

    def decode_m(match):
        utf8_sequence = match.group(0)
        utf8_bytes = utf8_sequence.encode("latin1").decode("unicode_escape").encode("latin1")
        return utf8_bytes.decode("utf-8")
    
    decoded_str = pattern.sub(decode_m, str)
    return decoded_str

def create_json_file() -> any:
    json_file = input("Please proide the input path for the JSON file: ")
    # Path to file: C:\Users\matth\OneDrive\Code\message_1.json
    json_file = json_file.replace('\\', '/')

    with open(json_file, 'r', encoding="utf-8") as file:
        json_data = json.load(file)
    
    return json_data

def initialize_fields(json_data) -> list[any]:
    participant_list = []

    participants = pd.json_normalize(json_data["participants"])
    names = participants["name"].tolist()

    for name in names:
        participant_list.append(
            {
                "name": name,
                "message_count": 0,
                "reaction_cont": 0,
                "media_count": 0
            }
        )

    messages = pd.json_normalize(json_data["messages"])

    return names, messages

#print(decode_utf8(messages.iloc[6,0]))
#print(names)
#print(messages)