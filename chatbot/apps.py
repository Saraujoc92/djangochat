from django.apps import AppConfig
from .chat_bot import start_chatbot

class ChatbotConfig(AppConfig):
    name = 'chatbot'

    def ready(self):
        start_chatbot()
        return True
    
