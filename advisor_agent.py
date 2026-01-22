import os
from typing import List, Optional
from models import EventCluster

class AdvisorAgent:
    """
    Intelligent Driver Advisor Agent.
    Interacts with LLMs (Mock or Real) to generate voice-enabled instructions.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        # Check if we should use Mock or Real
        self.use_mock = True if not api_key else False

    def generate_instruction(self, event_summary: EventCluster) -> str:
        """
        Takes a processed event summary and eventually feeds it to an LLM
        to produce a natural language instruction for the driver.
        """
        # 1. Deterministic Verification (Gap 2)
        # Check for safety overrides BEFORE asking LLM (or overriding its output)
        safety_override = self.verify_safety(event_summary)
        if safety_override:
            return safety_override

        # 2. QoS Adaptive Prompting (Gap 3)
        # If using real LLM, we'd inject this into the system prompt.
        # For mock, we modify the template.
        qos_context = ""
        # We don't have PDR in EventCluster directly (it was averaged), 
        # but let's assume we can infer strictness if urgency was penalized.
        # Or better, just check event type.
        
        instruction = ""
        if self.use_mock:
            instruction = self._mock_llm_response(event_summary)
        else:
            instruction = self._call_real_llm(event_summary)
            
        return instruction

    def verify_safety(self, event: EventCluster) -> Optional[str]:
        """
        Gap 2: Deterministic Verifier.
        Neuro-Symbolic check to prevent hallucinations.
        """
        # Rule: If Emergency Vehicle, MUST Yield. LLM cannot say "Speed up".
        if event.event_type == "Emergency Vehicle":
            return f"URA PRIORITY: Emergency vehicle approaching at {event.location}. Yield right of way immediately."
        
        # Rule: If Accident with High Priority, MUST Stop/Slow.
        if event.event_type == "Accident" and event.priority >= 5:
            return f"CRITICAL OVERRIDE: SEVERE ACCIDENT at {event.location}. HOST VEHICLE STOP REQUIRED."
            
        return None

    def _mock_llm_response(self, event: EventCluster) -> str:
        """
        Simulates an LLM response based on templates.
        """
        etype = event.event_type
        loc = event.location
        count = event.report_count

        # Gap 3: QoS Awareness
        # If report count is low (unverified) but priority is high, express uncertainty
        uncertainty_phrase = ""
        if event.report_count < 3 and event.priority > 3:
            uncertainty_phrase = " (Data unverified, exercise caution.)"

        if etype == "Accident":
            return f"Caution: Accident reported at {loc}.{uncertainty_phrase} Please slow down."
        elif etype == "Slippery Road":
            return f"Advisory: Slippery road conditions at {loc}.{uncertainty_phrase}"
        elif etype == "Congestion":
            return f"Traffic: Congestion at {loc}."
        elif etype == "Normal":
            return f"System: nominal."
        else:
            return f"Notice: {etype} at {loc}."

    def _call_real_llm(self, event: EventCluster) -> str:
        # Placeholder
        pass

    def analyze_scenario(self, event_list: List[EventCluster]) -> str:
        """
        Analyzes a list of events and prioritizes the single most critical instruction.
        """
        if not event_list:
            return "No active alerts. Drive safely."

        # Top priority event is first (list is sorted by processor)
        # We now check urgency score too.
        top_event = event_list[0]
        
        # Gap 4: Cognitive Load Check
        # If delivery mode is Visual/Silent, don't return voice string (or return marked string)
        if top_event.delivery_mode == "Silent":
            return "[SILENT] Logged low-priority event."
        
        if top_event.delivery_mode == "Visual":
            return f"[VISUAL ICON] {top_event.event_type} ahead."

        instruction = self.generate_instruction(top_event)
        return instruction
