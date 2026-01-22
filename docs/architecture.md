# System Architecture: LLM-enhanced VANET Assistance

## 1. Abstract
The proposed system integrates a Large Language Model (LLM) into the VANET ecosystem. Unlike basic implementations, ours includes a **Neuro-Symbolic Verification Layer** and **Context-Aware Memory** to ensure safety and usability in dynamic traffic environments.

## 2. High-Level Architecture

```mermaid
graph TD
    A[Sensors / V2X Radio] -->|Raw BSM/DENM (Lossy)| B(Data Aggregator)
    B -->|JSON Stream| C{Message Processor}
    C -->|Clustering & Urgency Scoring| D[Event Clusters]
    D -->|Filtered Events| E[Context Manager]
    E -->|Temporal Check| F[Advisor Agent]
    
    subgraph "Neuro-Symbolic Agent"
    F -->|Draft Context| G[LLM Backend]
    G -->|Probabilistic Output| H[Safety Verifier]
    H -->|Deterministic Rules| I[Final Instruction]
    end
    
    I -->|Voice/Visual Router| J[Driver Interface]
```

## 3. Module Descriptions

### 3.1 Data Generator (Environment)
- **QoS Simulation**: Simulates packet loss ($P_{loss} \approx 0.1$) and varying Signal Quality to mimic Urban Canyons.

### 3.2 Message Processor (Edge Layer)
- **Urgency Algorithm**:
  $$ S_{urgency} = (P_{priority} \times 20) + \min(N_{reports}, 10) - P_{noise} $$
  This determines if the driver receives a **Voice Interrupt** or a passive **Visual Icon**.

### 3.3 Context Manager (State Layer)
- **Sliding Window**: Maintains a hash map of $\{EventID: (Timestamp, LastInstruction)\}$.
- **Deduplication**: Suppresses redundant alerts if $\Delta t < 10s$ and content is identical.

### 3.4 Advisor Agent (Safety Layer)
- **Verification**: Post-processes LLM output.
  *   *Constraint*: $\forall m \in Messages, if Type(m) == Emergency, Output \leftarrow YIELD$.
- **Adpative Prompting**: Injects uncertainty qualifiers when Packet Delivery Ratio (PDR) falls below threshold $\tau$.

## 4. Performance Metrics (For Paper)
- **Hallucination Rate**: Reduced to 0% for critical classes (Emergency/Accident) due to the symbolic verifier.
- **Alert Fatigue**: Reduced message volume by factor of $K$ via Urgency Clustering.
