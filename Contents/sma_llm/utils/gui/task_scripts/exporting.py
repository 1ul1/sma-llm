"""Export conversation to PDF"""

from ..global_instances import get_CONVERSATION_UI
import subprocess

def export() -> None:
    """Shell commands directly"""
    command = ["osascript", "./sma_llm/utils/gui/task_scripts/ChooseWhereToSave.applescript"]
    try:
        save_path = subprocess.run(command, capture_output = True, text = True).stdout.strip()
    except:
        return

    with open(".history_tmp.txt", "w") as tmp:
        tmp.write(get_CONVERSATION_UI().history)

    command = f"cupsfilter .history_tmp.txt > '{save_path}.pdf'"
    try:
        subprocess.run(command, shell=True)
    finally:
        subprocess.run("rm .history_tmp.txt", shell=True)