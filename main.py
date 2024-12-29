from functions import *
import pandas as pd

json_data = create_json_file()

names, messages = initialize_fields(json_data)
filtered_messages = remove_self_message_notifications(messages)
filtered_messages.to_csv("filtered_messages.csv")

get_reaction_stats(messages, names)
get_media_stats(messages, names)
get_message_stats(messages, names)

print("*************************************************")
for name in names:
    print("Stats for " + name.get("name") + ":")
    print("Messages sent: " + str(name.get("message_count")))
    print("Reaction reacted: " + str(name.get("reaction_count")))
    print("Photos sent: " + str(name.get("photos_count")))
    print("Reels and posts sent: " + str(name.get("reels_posts_count")))
    print("Videos sent: " + str(name.get("video_count")))
    print("Audios sent: " + str(name.get("audio_count")))
    print(("*************************************************"))