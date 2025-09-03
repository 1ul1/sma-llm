class Memory:
    def __init__(self):
        # I use strings and not dictionaries for the implementation 
        # to be reused across different inference backends
        self.context = None
        self.conversation = None
        self.turn = None
    
    def set_context(self) -> None:
        self.context = input("Context: ") + "\nHere is the conversation so far:\nConversation history:"
        self.conversation = ""
        self.turn = True
    
    def update_memory(self, string: str) -> None:
        if self.turn is True:
            self.conversation = self.conversation + "\nUser: " + string
        else:
            self.conversation = self.conversation + "\nAssistant: " + string
        self.turn = not self.turn

    def get_history(self) -> str:
        pass
    