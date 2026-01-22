from data_generator import VanetDataGenerator
from message_processor import MessageProcessor
from advisor_agent import AdvisorAgent
import time
import json
import os

def main():
    print("=== LLM-based Driver Assistance System for VANET ===")
    
    # 1. Setup
    # Ask for API Key or use Mock
    # api_key = input("Enter OpenAI API Key (Press Enter for Mock Mode): ").strip()
    api_key = "" # Defaulting to Mock for automated run
    if not api_key:
        print("[System] Using Local/Mock LLM Mode.")
    
from context_manager import ContextManager

def main():
    print("=== LLM-based Driver Assistance System for VANET ===")
    
    # 1. Setup
    api_key = "" # Defaulting to Mock for automated run
    if not api_key:
        print("[System] Using Local/Mock LLM Mode.")
    
    agent = AdvisorAgent(api_key if api_key else None)
    generator = VanetDataGenerator(num_messages=50, packet_loss_ratio=0.1) # Simulate 10% loss
    processor = MessageProcessor()
    context_mgr = ContextManager()

    # 2. Simulation Loop
    # We will simulate 2 steps to test Context Memory
    for step in range(1, 3):
        print(f"\n[Step {step}] Listening for VANET messages...")
        time.sleep(1)
        
        # Generate batch
        generator.generate_batch('vanet_traffic_log.json')
        with open('vanet_traffic_log.json', 'r') as f:
            incoming_data = json.load(f)
        print(f"[System] Received {len(incoming_data)} raw messages.")

        # 3. Processing
        print(f"[Step {step}] Processing and Clustering data...")
        processed_events = processor.filter_messages(incoming_data)
        
        print(f"[System] Reduced to {len(processed_events)} unique event clusters.")
        for i, event in enumerate(processed_events[:3]):
            print(f"  - [{i+1}] {event.event_type} at {event.location} (Urgency: {event.urgency_score}, Mode: {event.delivery_mode})")

        # 4. LLM / Agent Advice
        print(f"[Step {step}] AI Advisor Generating Guidance...")
        
        # Get draft instruction from Agent
        top_event = processed_events[0] if processed_events else None
        
        if top_event:
            instruction = agent.analyze_scenario(processed_events)
            
            # Gap 1: Temporal Consistency Check
            if context_mgr.should_suppress(top_event, instruction):
                print(f"[Context Manager] Suppressing repeat instruction: '{instruction}'")
                final_output = "[SILENT] (Repeat info suppressed)"
            else:
                context_mgr.update_history(top_event, instruction)
                final_output = instruction

            print("\n" + "="*40)
            print(f"DRIVER OUTPUT ({top_event.delivery_mode}):")
            print(f"\"{final_output}\"")
            print("="*40 + "\n")

if __name__ == "__main__":
    main()
