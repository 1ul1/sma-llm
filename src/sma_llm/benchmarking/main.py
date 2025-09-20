"""Benchmarking pytorch vs mlcllm apple metal.
Most important metricts for an interactive chat:
Throughput: Total generation time                
            Total number tokens generated
Time to First Token:    Time between receiving prompts and producing first token

It will print these, in this order: model upload time, Time to First Token, throughput
"""
if __name__ == "__main__":
    from transformers import AutoTokenizer as Tokenizer # type: ignore
    from time import perf_counter
    from sma_llm.utils import Memory
    from .utils import *

    tokenizer = Tokenizer.from_pretrained("./sma_llm/models/hf_pytorch/tokenizer")

    testing_conversation = Memory()
    testing_conversation.update_memory("Can you explain why World War I started?")
    testing_conversation.update_memory("Sure! The main causes are often summarized as Militarism, Alliances, Imperialism, and Nationalism. Tensions between European powers, competing empires, and complex alliances made war more likely.")
    testing_conversation.update_memory("How did the alliances contribute?")
    testing_conversation.update_memory("When Austria-Hungary declared war on Serbia after the Archduke’s assassination, allied countries were pulled in. Russia supported Serbia, Germany backed Austria-Hungary, and France and Britain joined due to their alliances, turning a regional conflict into a world war.")
    question = "Can you summarize the main reasons World War I started in a concise paragraph?"

    assistant = None    # the model

    match input('what to test: "mlc" or "pytorch"'):
        case "mlc":
            assistant = MLCLLM()
        case "py":
            assistant = PyTorchTransformers()
        case _:
            raise ValueError("haven't selected anything")
    
    # getting parameters
    model_upload_time = assistant.upload_time

    time_to_first_token = assistant.generate_TTFT(testing_conversation)

    words_generated, total_generation_time = assistant.generate(testing_conversation)
    number_tokens_generated = len(tokenizer.encode(words_generated))

    throughput = number_tokens_generated / words_generated

    # sending them to STDOUT 
    print(f"""Engine Type: {assistant.type}
Model Upload Time: {model_upload_time}
Time to First Token: {time_to_first_token}
Throughput: {throughput}""")