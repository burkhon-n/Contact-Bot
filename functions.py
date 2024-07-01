import json
import time

def get_messages():
    with open("messages.json", "r") as json_file:
        return json.load(json_file)
    
def save_messages(messages):
    with open("messages.json", "w") as json_file:
        json.dump(messages, json_file, indent=4)

def get_id_with_guest(message_id):
    messages = get_messages()
    for i in range(len(messages)):
        if messages[i]['guest'] == message_id:
            return i
    return None
        
def get_id_with_admin(message_id):
    messages = get_messages()
    for i in range(len(messages)):
        if messages[i]['admin'] == message_id:
            return i
    return None

#clear messages in n days
def clear_messages(n):
    messages = get_messages()
    for i in range(len(messages)):
        if messages[i]['message']['date'] < (time.time() - n*24*60*60):
            messages.pop(i)
    save_messages(messages)