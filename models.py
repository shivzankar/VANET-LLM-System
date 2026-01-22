from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class VanetMessage:
    """
    Represents a single V2V or V2I communication message in a VANET network.
    """
    message_id: str
    timestamp: str
    msg_type: str  # BSM (Basic Safety Message) or DENM (Decentralized Environmental Notification)
    event: str     # e.g., 'Accident', 'Ice', 'Normal'
    location: str  # e.g., 'KM_20'
    content: str   # Raw payload/description
    priority: int  # 1 (Low) to 5 (Critical)
    speed: Optional[int] = 0
    packet_delivery_ratio: float = 1.0 # NEW: 0.0 to 1.0 (QoS metric)

    def to_dict(self):
        return self.__dict__

@dataclass
class EventCluster:
    """
    Represents an aggregated set of VANET messages pertaining to a single event/location.
    This reduces noise for the driver.
    """
    event_type: str
    location: str
    report_count: int
    timestamp: str          # Timestamp of the latest or first report
    priority: int           # Max priority in the cluster
    raw_content_sample: str # A representative message content
    message_ids: List[str] = field(default_factory=list)
    urgency_score: float = 0.0 # NEW: Calculated score for Cognitive Load management
    delivery_mode: str = "TBD" # NEW: "Voice", "Visual", or "Silent"

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "location": self.location,
            "report_count": self.report_count,
            "timestamp": self.timestamp,
            "priority": self.priority,
            "raw_content_sample": self.raw_content_sample,
            "urgency_score": self.urgency_score,
            "delivery_mode": self.delivery_mode
        }
