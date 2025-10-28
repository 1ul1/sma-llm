"""Change number of messages fed back to the model"""
from ..global_instances import get_CONVERSATION_UI

def retention(n: int) -> None:
    get_CONVERSATION_UI().memory.set_retention(n)
