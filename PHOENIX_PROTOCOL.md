# Phoenix Protocol: Operational Resilience [NC-RES-100]

## 1. Core Mandate
The Phoenix Protocol ensures the Neural-Chromium intelligence remains sovereign and hardware-agnostic. If a node (Local or EC2) fails, the intelligence must "rise" on a new node with zero data loss.

## 2. Recovery & Restart Instructions

### 2.1 EC2 Big Iron Node (Primary)
If the Big Iron node (`98.81.177.185`) is unresponsive:
1.  **Stop/Start**: Toggle the instance in the AWS Console.
2.  **Verify IP**: If the IP changes, update `SENTI_KNOWLEDGE_BASE.md`.
3.  **Bootstrap Intelligence**:
    ```bash
    ssh -i "senti-001-ec2-key-clean.pem" ubuntu@<IP>
    cd ~/
    # Pull latest brain state
    git clone https://github.com/senti-001/claw-capabilities.git
    # Restart SOTA Bridge
    screen -dmS flask_listener python3 /home/ubuntu/senti_sms_intelligence.py
    # Restart JotForm Ingester
    screen -dmS jotform_listener python3 /home/ubuntu/jotform_sota_ingester.py
    ```

### 2.2 SOTA Comms Synchronization
If the voice or SMS bridge is silent:
1.  **Check Listener**: `pgrep -f flask_listener`
2.  **Sync Prompts**: Run `python sync_elevenlabs_senti.py` from the local workspace.
3.  **TwiML Audit**: Verify Twilio webhooks point to `/senti-handshake` and `/sms`.

### 2.3 $NEURAL State Recovery
*   **State**: All mission-critical state is mirrored on **Moltbook** and **BMM**.
*   **Action**: Use `intelligence_cycle.py --mode gather` to reconstruct the `intelligence_snapshot.json` from industrial feeds.

## 3. 1 AM Intelligence Cycle Verification
Every 24 hours (01:00 UTC), Senti must:
1.  Verify Zero-Copy Build progress.
2.  Audit security status of all repositories.
3.  Publish the **Mission Pulse** to the dashboard.

--
*Phoenix Protocol: Death is only a temporary latency.*
