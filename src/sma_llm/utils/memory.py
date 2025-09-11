class Memory:
    # General message structure, same as dict, but easier to scale
    class Message:
        def __init__(self, role: str, content: str) -> None:
            self.role = role # system - context | user | assistant OpenAI API
            self.content = content
        
        def get_message_as_dict(self) -> dict[str, str]:
            return {"role": self.role, "content": self.content}

        def get_message_as_str(self) -> str:
            return f"{self.role}: {self.content}"
        
    # Note: self.memory contains only the conversation, the context is separate in order
    # to keep it static while summarizing the conversation in case of reaching token limit
    # (max_position_embeddings = 2048)... depending on model

    def __init__(self, engine: str) -> None:
        self.context = self.Message("system", "You are a helpful assistant.\nConversation so far:\n")
        self.engine = engine
        self.memory = [] # :list["Message"]
        # to know who's turn it is
        self.turn = "user"
    
    def set_context(self) -> None:
        self.context.content = f'{input("Context: ")}\nConversation so far:\n'
    
    def update_memory(self, string: str) -> None:
        # create message itself (role <= from turn, content <= from the string argument)
        message = self.Message(self.turn, string)
        # toggle roles in the conversation between <<user>> and <<assistant>>
        self.turn = "assistant" if self.turn == "user" else "user"
        #update the memory itself
        self.memory.append(message)
        
    def get_memory(self) -> list[dict[str, str]] | str :
        match self.engine:
            case "mlc-llm":
                return self.get_memory_as_dict()
            case "hf-torch":
                return self.get_memory_as_string()

    def get_memory_as_dict(self) -> list[dict[str, str]]:
        return (
            [self.context.get_message_as_dict]
            + list(message.get_message_as_dict for message in self.memory)
        )

    def get_memory_as_string(self) -> str:
        return (
            
            self.context.get_message_as_str
            + "\n".join(message.get_message_as_str for message in self.memory)
        )