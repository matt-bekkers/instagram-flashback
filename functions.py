import pandas as pd
import json

def create_json_file() -> list[any]:
    """
    Creates one json file from all provided files.

    Args:
        - None
    
    Returns:
        - A list of all JSON fields
    """

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
                "reaction_count": 0,
                "photos_count": 0,
                "reels_posts_count": 0,
                "video_count": 0,
                "audio_count": 0
            }
        )

    message_dataframes = []
    for item in json_data:
        messages = item.get("messages", [])
        
        if isinstance(messages, list) and messages:
            message_dataframes.append(pd.DataFrame(messages))

    message_dataframes = pd.concat(message_dataframes, ignore_index=True)

    return participant_list, message_dataframes

def remove_self_message_notifications(message_list: list[list[dict]]) -> list[dict]:
    """
    Since Instagram classifies notifications such as "xxx liked your message" as a sent message, this function removes them since the stats are still counted in the actual messages

    Args:
        - A list of messages
    
    Returns:
        - A list of filtered messages
    """
    unwanted_message_pattern = r"[a-zA-Z0-9]+ (changed|reacted|set|liked)"

    filtered_messages = message_list[~message_list["content"].str.contains(unwanted_message_pattern, na=False)]
    return filtered_messages
        
def get_reaction_stats(message_list, user_list):
    """
    Finds reaction fields within a list of messages.
    
    Args:
        - A list of messages
        - A list of users from the groupchat
    
    Returns:
        - None

    Preconditions:
        - Assumes all users in user_list are present in the groupchat
    """

    all_reactions = message_list["reactions"]

    all_reactions.dropna(inplace=True)

    for reaction_subset in all_reactions:
        for reaction in reaction_subset:
            user = reaction.get("actor")
            for person in user_list:
                if person.get("name") == user:
                    person["reaction_count"] += 1

    all_reactions.to_csv("reactions.csv")

def get_media_stats(message_list, user_list):
    """
    Updates the media_count field for each user

    Args:
        - A list of messages
        - A list of users

    Returns:
        - None
    """

    all_photos = pd.DataFrame(columns=["name", "photos"])

    all_posts_reels = pd.DataFrame(columns=["name", "posts_reels"])

    all_videos = pd.DataFrame(columns=["name", "videos"])

    all_audio = pd.DataFrame(columns=["name", "audio"])

    for row in message_list:
        all_photos["name"] = message_list["sender_name"]
        all_photos["photos"] = message_list["photos"]

        all_posts_reels["name"] = message_list["sender_name"]
        all_posts_reels["posts_reels"] = message_list["share"]

        all_videos["name"] = message_list["sender_name"]
        all_videos["videos"] = message_list["videos"]

        all_audio["name"] = message_list["sender_name"]
        all_audio["audio"] = message_list["audio_files"]

    
    photos_condition = all_photos.iloc[:, 1].isna()
    all_photos_filtered = all_photos[~photos_condition]

    for index, row in all_photos_filtered.iterrows():
        sender_name = row[0] 
        for user in user_list:
            if user.get("name") == sender_name:
                user["photos_count"] += 1

    posts_reels_condition = all_posts_reels.iloc[:, 1].isna()
    all_posts_reels_filtered = all_posts_reels[~posts_reels_condition]

    for index, row in all_posts_reels_filtered.iterrows():
        sender_name = row[0] 
        for user in user_list:
            if user.get("name") == sender_name:
                user["reels_posts_count"] += 1

    videos_condition = all_videos.iloc[:, 1].isna()
    all_videos_filtered = all_videos[~videos_condition]

    for index, row in all_videos_filtered.iterrows():
        sender_name = row[0] 
        for user in user_list:
            if user.get("name") == sender_name:
                user["video_count"] += 1

    audio_condition = all_audio.iloc[:, 1].isna()
    all_audio_filtered = all_audio[~audio_condition]

    for index, row in all_audio_filtered.iterrows():
        sender_name = row[0] 
        for user in user_list:
            if user.get("name") == sender_name:
                user["audio_count"] += 1

def get_message_stats(message_list, user_list):
    unwanted_message_pattern = r"[a-zA-Z0-9]+ sent"

    raw_messages = message_list[~message_list["content"].str.contains(unwanted_message_pattern, na=False)]

    all_messages = pd.DataFrame(columns=["name", "message"])
    for row in message_list:
        all_messages["name"] = message_list["sender_name"]
        all_messages["message"] = message_list["content"]
    
    message_condition = all_messages.iloc[:, 1].isna()
    all_messages_filtered = all_messages[~message_condition]

    for index, row in all_messages_filtered.iterrows():
        sender_name = row[0]
        for user in user_list:
            if user.get("name") == sender_name:
                user["message_count"] += 1