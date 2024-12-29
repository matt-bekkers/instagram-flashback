from functions import *
import sys

out = sys.stdout

# C:\Users\matth\OneDrive\Code\instagram-flashback\message_1.json
# C:\Users\matth\OneDrive\Code\instagram-flashback\message_2.json
json_data = create_json_file()

names, messages = initialize_fields(json_data)

messagesdf = pd.DataFrame(messages)

out.write(str(names))
#print("--------------------------------------------------------------------------------")
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    out.write(str(messages))