from agent import agent_decide

print("🤖 Agentic AI Started (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    print("You:", user_input)
    if user_input.lower() == "exit":
        break

    response = agent_decide(user_input)
    print("Agent:", response)
