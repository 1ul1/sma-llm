"""global instances."""

# The GUI app
_FRONTEND = None
# The Conversation instance used, "_UI" cause it was added specifically for the GUI
_CONVERSATION_UI = None

def set_CONVERSATION_UI(obj) -> None:
    global _CONVERSATION_UI 
    _CONVERSATION_UI = obj

def get_CONVERSATION_UI():
    return _CONVERSATION_UI

def get_FRONTEND():
    return _FRONTEND

def start_GUI():
    from .frontend import Frontend
    from sma_llm.utils.io_pipeline.handle_write.write_UI import WriteUI
    from sma_llm.utils.io_pipeline import set_SHOW

    set_SHOW(WriteUI())
    
    global _FRONTEND
    _FRONTEND = Frontend()
    _FRONTEND.run()

def start_wait_screen():
    from .wait_screen import WaitScreen
    WaitScreen()