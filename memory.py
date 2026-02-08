conversation_memory = []

def add_to_memory(role, content):
    conversation_memory.append(
        {"role": role, "content": content}
    )

def get_memory():
    return conversation_memory

def clear_memory():
    conversation_memory.clear()
