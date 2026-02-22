from multi_model_refiner.crew import MultiModelRefinerCrew
from multi_model_refiner.tools.custom_tool import memory_tool

def run():
    print("==================================================")
    print("== Welcome to the Bulletproof Conversational Crew! ==")
    print("==================================================")
    print("Enter your research topic below. Type 'exit' to end.")
    print("\n")

    while True:
        topic = input("Topic: ")

        if topic.lower() in ['exit', 'quit']:
            print("Session ended. Goodbye!")
            break

        if topic:
            # 1. PYTHON retrieves the memory BEFORE the AI starts
            print("\n[*] Searching memory...")
            past_context = memory_tool.retrieve_memory(topic)
            
            # Pass the memory directly into the variables for the AI
            inputs = {
                'topic': topic,
                'past_context': past_context
            }

            # 2. Kick off the crew
            result = MultiModelRefinerCrew().crew().kickoff(inputs=inputs)
            
            print("\n\n########################")
            print("## Here is the Refined Result:")
            print("########################\n")
            print(result.raw)
            print("\n\n")

            # 3. PYTHON saves the memory AFTER the AI finishes
            print("[*] Saving new insights to memory...")
            memory_tool.save_memory(f"Topic: {topic}\nFindings: {result.raw}")
            print("[*] Save complete.\n")
        else:
            print("Please enter a topic to research.")