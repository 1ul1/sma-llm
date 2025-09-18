# Speech Memory Assistant
## Project Layout
```mermaid
SMA-LLM
    LICENSE
    README.md
    env.yaml
    src
        memory_management_scripts
            memory_safety.sh
            run.sh
            terminate_model.sh
        sma_llm
            __init__.py
            utils
                io_pipeline
                    __init__.py
                    handle_read
                        __init__.py
                        read_global_instance.py
                        read_input.py
                        keyboard.py
                    handle_write
                        __init__.py
                        write_global_instance.py
                        write_output_interface.py
                        speak_output.py
                        print_output.py
                memory.py
                network
                    network_pytorch_hf.py
                    network_interface.py
                    network_mlc_llm.py
                    __init__.py
                    read_model_config.py
                __init__.py
                text_handler.py
            models
                download.py
                models.md
            main
                chat
                    chat_main.py
                    conversation.py
                    __init__.py
                __init__.py
                my_main.py
```
## Project Flow
```mermaid
python3 -m sma_llm.main.my_main

my_main -> Initialize a chat -> Upload the "Assistant"'s model
            Conversation()   
                             -> Initialize the chat's memory

        -> Converse -> read, process & autocorrect input
        |           -> update chat memory
        |           -> generate Assistant's answer & live print it
        |           -> process & autocorrect the output
        |           -> update chat memory
        |           -> recursively repeat Converse()---|
        |______________________________________________|
                 
```