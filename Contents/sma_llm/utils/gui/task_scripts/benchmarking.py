"""Print live metricts for the interactive chat.
Time to First Token
Throughput"""

from sma_llm.benchmarking.main import main
from ..chat_bubble import ChatBubble
from ..global_instances import get_FRONTEND

def benchmark() -> None:
    get_FRONTEND().message_layout.addWidget(ChatBubble(string = main(True)))