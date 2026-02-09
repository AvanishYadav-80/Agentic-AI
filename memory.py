# memory.py

# Global conversation memory
memory = []

def add_to_memory(role, content):
    memory.append({"role": role, "content": content})

def get_memory():
    return memory

def clear_memory():
    memory.clear()

def trim_memory(max_turns):
    """
    Keep system messages + last N user/assistant messages
    """
    global memory

    # Always keep system messages
    system_messages = [m for m in memory if m["role"] == "system"]

    # Keep recent conversation only
    conversation = [m for m in memory if m["role"] != "system"]

    memory = system_messages + conversation[-max_turns:]
