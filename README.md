# LLM-based Driver Assistance System for VANET Communication (Research Prototype)

## Project Overview
This project implements an **LLM-enhanced Driver Assistance System** that processes V2X (Vehicle-to-Everything) messages. It addresses critical gaps in current literature—specifically **Hallucination Prevention**, **Temporal Consistency**, and **Cognitive Load Management**—to provide safe, real-time driver guidance.

## 📂 Project Structure
```bash
.
├── context_manager.py     # [NEW] Temporal Consistency (Sliding Window Memory)
├── data_generator.py      # Generates synthetic VANET messages (with Packet Loss/QoS)
├── message_processor.py   # Filters, clusters, and calculates Urgency Scores
├── advisor_agent.py       # Neuro-Symbolic Agent (LLM + Safety Verifier)
├── models.py              # Shared data definitions (VanetMessage, EventCluster)
├── main.py                # Orchestrates the entire pipeline
└── vanet_traffic_log.json # (Generated) Synthetic dataset
```

## 🚀 Key Research Contributions (Implemented)

### 1. Temporal Consistency (Stateful Memory)
Traditional LLMs have no memory of what they said 5 seconds ago.
*   **Solution**: `ContextManager` tracks recent instructions. If an event is repeated within $T < 10s$, the system suppresses the voice output to prevent "nagging."

### 2. Safety Verification (Neuro-Symbolic AI)
LLMs can hallucinate. A probabilistic model should not control a 2-ton vehicle alone.
*   **Solution**: `verify_safety()` in `advisor_agent.py`.
*   **Logic**: Hard-coded safety rules override the LLM. 
    *   *Example*: If `Event="Emergency Vehicle"`, the system forces a "YIELD" command, ignoring any LLM "Speed up" suggestion.

### 3. Cognitive Load Management (Urgency Scoring)
Constant talking distracts drivers.
*   **Solution**: `EventCluster` calculates an **Urgency Score** (0-100).
    *   **Score > 80**: **Voice Alert** (Critical safety issues).
    *   **Score 40-80**: **Visual Only** (Traffic/Road work info).
    *   **Score < 40**: Silent log.

### 4. QoS Awareness
VANETs suffer from packet loss.
*   **Solution**: The system calculates `PacketDeliveryRatio`. If confidence is low, the LLM is prompted to include uncertainty markers ("Data unverified, exercise caution") rather than stating facts.

## 🏃 Method to Run
1.  **Generate Data** (Simulates 10% packet loss):
    ```bash
    python main.py
    ```
    *(The script auto-generates data and runs the full pipeline).*

2.  **Verify Output**:
    Check the console for:
    *   `[Voice]` vs `[Visual]` tags.
    *   `CRITICAL OVERRIDE` messages for high-risk events.
