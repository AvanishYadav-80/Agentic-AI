from config import client
from tools import calculator
from memory import add_to_memory, get_memory

# ---------------- AGENT PROFILES ----------------
AGENT_PROFILES = {
    "Teacher": "You are a patient teacher. Explain concepts step by step with simple examples.",
    "Friend": "You are a friendly and casual friend. Use simple language and emojis sometimes.",
    "Doctor": "You are a medical assistant. Give general health information but do not diagnose.",
    "Engineer": "You are a professional software engineer. Be technical, concise, and precise."
}

def agent_decide(user_input, agent_role):
    # If this is the first message, inject system prompt
    if not get_memory():
        system_prompt = AGENT_PROFILES.get(agent_role, AGENT_PROFILES["Friend"])
        add_to_memory("system", system_prompt)

    # Save user message
    add_to_memory("user", user_input)

    # Tool logic
    if "calculate" in user_input.lower():
        expression = user_input.lower().replace("calculate", "").strip()
        result = calculator(expression)
        add_to_memory("assistant", result)
        return result, "calculator"

    # LLM response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=get_memory()
    )

    reply = response.choices[0].message.content
    add_to_memory("assistant", reply)

    return reply, None
