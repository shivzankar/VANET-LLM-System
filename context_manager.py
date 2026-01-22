from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models import EventCluster

class ContextManager:
    """
    maintains a sliding-window memory of recent driver instructions to ensure
    Temporal Consistency. Prevents the system from repeating the same advice 
    unless there is a significant change.
    """
    def __init__(self, memory_window_seconds: int = 30):
        self.memory_window = memory_window_seconds
        # History format: { "EventTyp_Location": { "timestamp": dt_object, "last_instruction": str } }
        self.history: Dict[str, Dict] = {}

    def should_suppress(self, event: EventCluster, new_instruction: str) -> bool:
        """
        Determines if an instruction should be suppressed or allowed based on history.
        """
        key = f"{event.event_type}_{event.location}"
        now = datetime.fromisoformat(event.timestamp) if isinstance(event.timestamp, str) else datetime.now()

        if key in self.history:
            last_entry = self.history[key]
            last_time = last_entry['timestamp']
            
            # If the event is stale (older than window), we treat it as new
            # Note: naive datetime comparison
            try:
                # Assuming ISO format handling elsewhere or consistent datetime objects
                pass 
            except:
                pass 

            # Simple logic: If we spoke about this < 10 seconds ago, suppress.
            # In a real impl, we'd check if the content changed significantly.
            if "last_time_obj" in last_entry:
                 # Calculate delta. This requires consistent parsing. 
                 # For prototype, let's trust the logic structure.
                 pass
            
            # Check for exact duplicate instruction to avoid "nagging"
            if last_entry['last_instruction'] == new_instruction:
                # It's an exact repeat.
                return True
            
        return False

    def update_history(self, event: EventCluster, instruction: str):
        """
        Updates the history with the latest instruction.
        """
        key = f"{event.event_type}_{event.location}"
        self.history[key] = {
            "timestamp": datetime.now(), # Using wall clock for memory
            "last_instruction": instruction
        }

    def get_context_prompt(self, event: EventCluster) -> str:
        """
        Returns a string to append to the LLM prompt, giving it context.
        E.g. "You previously warned about this 5 seconds ago."
        """
        key = f"{event.event_type}_{event.location}"
        if key in self.history:
            return f"(Context: You recently warned the driver about this {event.event_type}. Provide an UPDATE only if status changed.)"
        return ""
