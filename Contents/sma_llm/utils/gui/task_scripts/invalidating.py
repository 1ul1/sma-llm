"""Print Message if an invalid command was triggered."""
from ..chat_bubble import ChatBubble
from ..global_instances import get_FRONTEND

def invalid():
    get_FRONTEND().message_layout.addWidget(ChatBubble(string="Invalid Command"))