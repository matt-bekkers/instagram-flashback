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

def create_json_file() -> list[any]:

    # Instagram JSON message files are limited to 10 000 messages/file, so we ask the user how many files they want to pass
    n_files = int(input("How many JSON files to be passed?: "))

    files = []
    for i in range(n_files):
        json_file = input("Please proide the input path for the JSON file " + str(i + 1) + ": ")
        json_file = json_file.replace('\\', '/')
       
        with open(json_file, 'r', encoding="utf-8") as open_file:
            json_data = json.load(open_file)
            files.append(json_data)

    
    return files


def initialize_fields(json_data: list) -> tuple[list[dict], list, list]:
    """
    Inits participant, message, reaction fields. Returns a tuple of these 3 fields.

    Args:
        - json_data: list of loaded JSON data
    
    Returns:
        - list of dictionaries for each participant's stats
    """


    participant_list = []

    # Must assume that participants remain the same thoughout the files
    participants = json_data[0].get("participants", [])
    names = [participant["name"] for participant in participants]

    for name in names:
        participant_list.append(
            {
                "name": name,
                "message_count": 0,
                "reaction_cont": 0,
                "media_count": 0
            }
        )

    #messages = pd.json_normalize(json_data["messages"])
    message_dataframes = []
    for item in json_data:
        messages = item.get("messages", [])
        
        if isinstance(messages, list) and messages:
            message_dataframes.append(pd.DataFrame(messages))

    message_dataframes = pd.concat(message_dataframes, ignore_index=True)

    return names, message_dataframes

#print(decode_utf8(messages.iloc[6,0]))
#print(names)
#print(messages)