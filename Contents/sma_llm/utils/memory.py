class Memory:
    """All data sturctures and logic behind the conversation history and context."""
    # General message structure, same as dict, but easier to scale
    class Message:
        def __init__(self, role: str, content: str) -> None:
            self.role = role # system - context | user | assistant OpenAI API
            self.content = content
        
        @property
        def message_as_dict(self) -> dict[str, str]:
            return {"role": self.role, "content": self.content}
        
        @property
        def message_as_str(self) -> str:
            return f"{self.role}: {self.content}"
        
    # Note: self.memory contains only the conversation, the context is separate in order
    # to keep it static while summarizing the conversation in case of reaching token limit
    # (max_position_embeddings = 2048)... depending on model

    def __init__(self) -> None:
        self.context = self.Message("system", "You are a helpful assistant.\nConversation so far:\n")
        self.memory = [] # :list["Message"]
        self.retention = 4 # how many messages are fed to the LLM
        self.turn = "user"
    
    def set_context(self) -> None:
        self.context.content = f'{input("Context: ")}\nConversation so far:\n'

    def set_retention(self, retention: int) -> None:
        self.retention = retention
    
    def update_memory(self, string: str) -> None:
        # create message itself (role <= from turn, content <= from the string argument)
        message = self.Message(self.turn, string)
        # toggle roles in the conversation between <<user>> and <<assistant>>
        self.turn = "assistant" if self.turn == "user" else "user"
        #update the memory itself
        self.memory.append(message)

    def forget(self) -> None:
        """Useful when generation is stopped before finishing."""
        self.memory = self.memory[:-1]
        self.turn = "assistant" if self.turn == "user" else "user"
    
    def get_memory(self, obj = None) -> list[dict[str, str]] | str | None: # obj: Network
        from sma_llm.utils.network import MLCLLM, PyTorchTransformers
        match obj:
            case MLCLLM():
                return self.memory_as_dict
            case PyTorchTransformers():
                return self.memory_as_string
            case _:
                print(self.memory_as_string, end="", flush=True)
                return self.memory_as_string

    @property
    def memory_as_dict(self) -> list[dict[str, str]]:
        return (
            [self.context.message_as_dict]
            + [message.message_as_dict for message in self.memory[-(self.retention * 2):]]
        )

    @property
    def memory_as_string(self) -> str:
        return (
            self.context.message_as_str
            + "\n".join(message.message_as_str for message in self.memory[-(self.retention * 2):])
        )
    
    @property
    def full(self) -> str:
        return (
            self.context.message_as_str
            + "\n".join(message.message_as_str for message in self.memory)
        )