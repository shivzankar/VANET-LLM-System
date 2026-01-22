from datetime import datetime
from typing import List, Optional
import json
import random
from models import VanetMessage

class VanetDataGenerator:
    """
    Simulates the generation of V2V/V2I messages in a vehicular network.
    
    Attributes:
        num_messages (int): Number of base messages to generate.
        message_types (list): Supported message standards (BSM, DENM).
        events (list): Possible road events (Accident, Congestion, etc.).
        locations (list): Discrete locations for simulation (KM_10, KM_15...).
    """
    
    def __init__(self, num_messages: int = 100, packet_loss_ratio: float = 0.0):
        self.num_messages = num_messages
        self.packet_loss_ratio = packet_loss_ratio # 0.0 to 1.0
        self.message_types = ['BSM', 'DENM'] 
        self.events = ['Accident', 'Congestion', 'Slippery Road', 'Road Works', 'Normal', 'Emergency Vehicle']
        self.locations = [f"KM_{i}" for i in range(10, 50, 5)] 

    def generate_message(self) -> Optional[VanetMessage]:
        """
        Generates a single random VANET message with realistic attributes.
        Returns None if packet is 'lost'.
        """
        # Simulate Packet Loss
        if random.random() < self.packet_loss_ratio:
            return None

        msg_type = random.choice(self.message_types)
        
        # BSM is usually high frequency status updates, DENM is event driven
        if msg_type == 'BSM':
            content = "Vehicle status normal"
            event = "Normal"
            priority = 1
        else:
            event = random.choice(self.events)
            if event == 'Normal': # Re-roll if DENM gets normal
                event = random.choice(self.events[0:-2])
            content = f"Alert: {event} detected"
            priority = random.randint(2, 5)

        # Simulate Signal Quality / Packet Delivery Ratio
        # In urban canyons, this fluctuates.
        pdr = round(random.uniform(0.4, 1.0), 2) 

        return VanetMessage(
            message_id=f"msg_{random.randint(1000, 9999)}",
            timestamp=datetime.now().isoformat(),
            msg_type=msg_type,
            event=event,
            location=random.choice(self.locations),
            speed=random.randint(0, 120),
            priority=priority,
            content=content,
            packet_delivery_ratio=pdr
        )

    def generate_batch(self, output_file: str = 'vanet_traffic_log.json') -> None:
        """
        Generates a batch of messages, introduces bursty traffic (duplicates),
        and saves to a JSON file.
        """
        messages: List[VanetMessage] = []
        
        # Base generation
        for _ in range(self.num_messages):
            msg = self.generate_message()
            if msg:
                messages.append(msg)
        
        # Introduce duplicates/bursts to simulate real VANET floods
        if len(messages) > 10:
            burst_msg = messages[5] 
            for _ in range(10): 
                duplicate = VanetMessage(
                    message_id=f"msg_{random.randint(1000, 9999)}",
                    timestamp=datetime.now().isoformat(),
                    msg_type=burst_msg.msg_type,
                    event=burst_msg.event,
                    location=burst_msg.location,
                    speed=burst_msg.speed,
                    priority=burst_msg.priority,
                    content=burst_msg.content,
                    packet_delivery_ratio=burst_msg.packet_delivery_ratio # Same env conditions
                )
                messages.append(duplicate)
        
        random.shuffle(messages)
        data = [msg.to_dict() for msg in messages]

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Generated {len(data)} synthetic VANET messages in {output_file} (Loss Ratio: {self.packet_loss_ratio})")

if __name__ == "__main__":
    generator = VanetDataGenerator(num_messages=50)
    generator.generate_batch()
