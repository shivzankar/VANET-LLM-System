from datetime import datetime
import collections
from typing import List, Dict
from models import VanetMessage, EventCluster

class MessageProcessor:
    """
    Handles the ingestion, filtering, and clustering of raw VANET messages.
    """
    
    def __init__(self, output_file: str = 'processed_clusters.json'):
        self.output_file = output_file

    def filter_messages(self, raw_data: List[Dict]) -> List[EventCluster]:
        """
        Deduplicates messages based on content and location/timestamp proximity.
        Returns a list of unique 'EventCluster' objects.
        
        Args:
            raw_data: List of dictionary representations of VanetMessages.
        """
        # Convert dicts back to objects for easier handling if needed,
        # or just process dicts. Here we will use the dicts but output Clusters.
        
        clusters = collections.defaultdict(list)
        
        for msg_dict in raw_data:
            # Key: Event Type + Location (e.g., "Accident_KM_20")
            # In a real system, we'd use a sliding time window (delta t < 5s)
            key = f"{msg_dict['event']}_{msg_dict['location']}"
            clusters[key].append(msg_dict)

        processed_events: List[EventCluster] = []

        for key, msg_list in clusters.items():
            base_msg = msg_list[0]
            count = len(msg_list)
            
            # Map valid attributes to EventCluster
            # Calculate Urgency Score (Cognitive Load Management)
            # Factor 1: Event Priority (1-5) -> 20 pts each
            # Factor 2: Report Count (Confidence) -> Max 10 pts
            # Factor 3: QoS (Packet Delivery Ratio) -> If data is reliable, we trust it more
            
            avg_pdr = sum(m.get('packet_delivery_ratio', 1.0) for m in msg_list) / count
            
            urgency = (base_msg['priority'] * 18) + (min(count, 10))
            if avg_pdr < 0.5:
                # Penalty for low QoS - don't distract driver with unreliable info?
                # OR: Warning should be cautious. 
                # For "Urgency" (interrupting driver), we might lower score if unverified.
                urgency *= 0.8
            
            # Determine Delivery Mode
            # Threshold > 80: Voice (Critical)
            # Threshold 40-80: Visual (Advisory)
            # Threshold < 40: Silent/Log
            if urgency > 80:
                mode = "Voice"
            elif urgency > 40:
                mode = "Visual"
            else:
                mode = "Silent"
                
            cluster = EventCluster(
                event_type=base_msg['event'],
                location=base_msg['location'],
                report_count=count,
                timestamp=base_msg['timestamp'],
                priority=base_msg['priority'],
                raw_content_sample=base_msg['content'],
                message_ids=[m['message_id'] for m in msg_list],
                urgency_score=round(urgency, 1),
                delivery_mode=mode
            )
            processed_events.append(cluster)
            
        # Sort by urgency (descending)
        processed_events.sort(key=lambda x: x.urgency_score, reverse=True)
        return processed_events

if __name__ == "__main__":
    import json
    try:
        with open('vanet_traffic_log.json', 'r') as f:
            raw_data = json.load(f)
            processor = MessageProcessor()
            summary = processor.filter_messages(raw_data)
            print(json.dumps([c.to_dict() for c in summary], indent=2))
    except FileNotFoundError:
        print("Run data_generator.py first.")
