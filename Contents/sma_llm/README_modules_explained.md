# SMA - Architecture.

## Network - Unified LLM abstract class

The LLM frameworks implement on this to guarantee identical behaviour. They are **singletons** whose instances only exist when the models are loaded onto memory and ready to run.

## Memory class

It is general purpose and saves each message as an instance of a class that saves its *role* and *content*. The conversation history itself is a list of such objects.

The class is general purpose, as this logic facilitates its use with either dictionaries or formated strings for inference.

## IO_pipeline

-> Abstract classes for read and write logic;

-> Global Variables with getters and setters, used throughout the project to handle IO;

Adding or changing logic for the entire project takes minimal changes and does not require touching anything else other than this package.

### Read

The **read** package holds the abstract class with the generic read method definition.

Input can be processed from keyboard or from audio via the __Speech to Text__ feature - it uses Whisper by OpenAI under the hood and ffmpeg to gather microphone input.

*Note*: The project also runs a bash script to create a RAM disk image formated with a filesystem. The audio file can be saved directly on RAM. This avoids repeated writes on SSD and ensures the fastest read and processing for the STT. Interruption and kill signals are caught in *my_main.py*, the starting module of the project, to trigger the execution of the bash script that dismounts and erases the disk image, cleaning everything up.
### Write

The **write** package holds the abstract class with the generic write method definition.

Output can be displayed by normal stdout, by a chat bubble on the GUI and by __Text to Speech__ - uses Python ObjectiveC bridge (PyObjC)

## Text  Handling

The class presents several methods to process strings, using standard Python string methods and RegEx. It also has a simple autocorrect.

Text Handling is used especially for running the PyTorch models, which allow access to the Tokenizer and the raw generate() method. The generation in this project is adapted to output live. For small models it is essential to process each live output before refeeding it to the generation() call, as small models are prone to hallucinate. This way, the "hallucination" is somewhat contained and corrected before badly influencing further generation, highly increasing overall accuracy.

Text Handling also has a general purpose stop() method that breaks generation after *n* sentences.

## Conversation

This module puts all the logic together to create an open-ended like conversation with a LLM model.

## Benchmarking

The package has the main script for reliably calculating relevant parameters such as: Model Upload Time, Time to First Token and Throughput.

Memory use is also calculated with a bash script. Due to the way the OS reports memory use and how it handles it, the memory usage data has limitations, but it provides useful context for the overall trends.

[bash script used to calculate used RAM during upload, generation and after termination](./Contents/sma_llm/benchmarking/scripts/get_memory.sh)

**Note**: It is difficult to determine exact RAM usage, but there was a significant difference between the 2 frameworks. MLC-LLM seemed to push the system's RAM to 18 GB out of 24 GB and trigger 2-3 GB Swap Mem, while PyTorch with MPS would push system's RAM to 22-23 GB and trigger as much as 10 GB Swap. Memory Pressure would rarely reach medium levels for MLC-LLM, but quickly reach high levels during PyTorch inference. Because of this I created the *memory_management_scripts* directory to watch for RAM levels and terminate the process before the OS would start allocating SWAP.