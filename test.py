from google.generativeai.types.content_types import StrictContentType
from typing import Iterable, Union, List, Dict, Any

class AiChatHistory: 
    def __init__(self, data:str): 
        self.data = data

    def __str__(self): 
        attrs = {}
        for key, value in self.__dict__.items(): 
            if hasattr(value, '__dict__') and not isinstance(value, (int, float, str, list, tuple, dict)): 
                attrs[key] = value.__dict__
            else:
                attrs[key] = value

        pretty_attrs = json.dumps(attrs, indent=2).replace("null", "None")
        return f"AiChatHistory {pretty_attrs}"

    from google.generativeai.types import generation_types

    def parse_geminichat_history(
        gemini_chat_history: generation_types.GenerateContentResponse
    ) -> Iterable[Dict]: 
        gemini_chat_history_items = []

        for content in gemini_chat_history: 
            gemini_chat_history_items.append({
                "role": content.role,
                "parts": [
                    { "text": part.text } for part in content.parts
                ]
            })
        return gemini_chat_history_items

    def get_history(self, chat_title:str = "") -> dict: 
        b64_history = bytes(self.data, "utf-8")
        decompressed_history = zlib.decompress(
            b64decode(b64_history)
        )
        history = json.loads(decompressed_history.decode())
        
        if chat_title: 
            return history.get(chat_title, history)

        return history

    def set_history(
        gemini_chat_history: Union[Iterable[genai.types.StrictContentType], Dict], 
        chat_title:str
    ) -> None: 

        history = self.data
        history[chat_title] = parse_geminichat_history(gemini_chat_history)
        # print(json.dumps(history))
        # print()

        bytes_history = bytes(json.dumps(history), "utf-8")
        compressed_history = zlib.compress(bytes_history)
        b64_history = b64encode(compressed_history).decode()
        user["history"] = b64_history

class WhatsAppUser: 
    def __init__(self, id, history, selected_chat): 
        self.id = id
        self.ai_chat_history = AiChatHistory(history)
        self.selected_chat = selected_chat

    def __str__(self): 
        attrs = {}
        for key, value in self.__dict__.items(): 
            if hasattr(value, '__dict__') and not isinstance(value, (int, float, str, list, tuple, dict)): 
                attrs[key] = value.__dict__
            else:
                attrs[key] = value
        
        pretty_attrs = json.dumps(attrs, indent=2).replace("null", "None")
        return f"WhatsAppUser {pretty_attrs}"

users = get_users("./wa_users.json")

for id, item in users.items(): 
    wa_user = WhatsAppUser(id, **item)
    print(wa_user)

print(wa_user.ai_chat_history)
# wa_user = WhatsAppUser(id, history, selected_chat)
# user = users["6281818475959"]

# WhatsAppUser(
#     id={self.id}, 
#     history={self.history}, 
#     selected_chat={self.selected_chat} 
# }