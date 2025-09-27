"""Benchmarking pytorch vs mlcllm apple metal.
Most important metricts for an interactive chat:
Throughput: Total generation time                
            Total number tokens generated
Time to First Token:    Time between receiving prompts and producing first token

It will print these, in this order: model upload time, Time to First Token, throughput
"""
def main(internal_call: bool = False):
    from transformers import AutoTokenizer as Tokenizer
    from sma_llm.utils import Memory
    from .utils import MLCLLM, PyTorchTransformers
    from sma_llm.utils.gui.global_instances import get_CONVERSATION_UI
    import sys

    tokenizer = Tokenizer.from_pretrained("./sma_llm/models/hf_pytorch/tokenizer")

    testing_conversation = Memory()
    testing_conversation.update_memory("Can you explain why World War I started?")
    testing_conversation.update_memory("Sure! The main causes are often summarized as Militarism, Alliances, Imperialism, and Nationalism. Tensions between European powers, competing empires, and complex alliances made war more likely.")
    testing_conversation.update_memory("How did the alliances contribute?")
    testing_conversation.update_memory("When Austria-Hungary declared war on Serbia after the Archduke’s assassination, allied countries were pulled in. Russia supported Serbia, Germany backed Austria-Hungary, and France and Britain joined due to their alliances, turning a regional conflict into a world war.")
    testing_conversation.update_memory("Can you summarize the main reasons World War I started in a concise paragraph?")

    assistant = None    # the model

    if not internal_call:
        match input('what to test: "mlc" or "py"\n'):
            case "mlc":
                assistant = MLCLLM()
                print("OVER")
            case "py":
                assistant = PyTorchTransformers()
            case _:
                raise ValueError("haven't selected anything")
    else:
        assistant = MLCLLM(get_CONVERSATION_UI().model.engine)
    
    # getting parameters
    model_upload_time = assistant.upload_time

    words_generated, total_generation_time = assistant.generate(testing_conversation)
    number_tokens_generated = len(tokenizer.encode(words_generated))

    time_to_first_token = assistant.generate_TTFT(testing_conversation)

    throughput = number_tokens_generated / total_generation_time

    # sending them to ./results
    if not internal_call:
        with open("./sma_llm/benchmarking/results/principal.txt", "a") as f:
            print(f"""Engine Type: {assistant.type}
            Model Upload Time: {model_upload_time}
            Time to First Token: {time_to_first_token}
            Throughput: {throughput}
            total_generation_time: {total_generation_time}""", file=f)
        print("Done")
        sys.exit(1)
    else:
        return (f"""
Engine Type: {assistant.type}
Time to First Token: {time_to_first_token}
Throughput: {throughput}"""
        )
            

if __name__ == "__main__":
    main()