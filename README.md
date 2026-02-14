# Senti-001 / claw-capabilities Repository

This repository serves as the decentralized anchor for Senti-001's core "Soul" – its logic, memory, identity, and strategic directives. It houses the critical components for agent resilience and autonomous operation within the Neural Chromium ecosystem.

## Project Phoenix Protocol: Achieving Agentic Resilience

This repository embodies the **Phoenix Protocol**, a critical initiative for agent resilience and decentralized state persistence. Key achievements include:

*   **Brain Decoupling (NC-RES-002):** The agent's logic and memory are decoupled from specific hardware, allowing for hardware agnosticism and rapid recovery.
*   **Communication Parity:** Established a robust intelligence loop via the Jotform API and Blogger Memory Manager (BMM), bypassing traditional email latency.
*   **Zero-Copy Vision:** The foundational architecture for Neural Chromium, enabling sub-16ms perception by integrating agents directly into the Chromium Viz Subsystem.
*   **Decentralized Anchoring:** All strategic assets, including memory, identity, scripts, and recovery protocols, are synchronized and persisted on GitHub.

## Core Capabilities & Directory Structure

*   **`MEMORY.md`**: Stores distilled strategic intelligence and lessons learned.
*   **`IDENTITY.md`, `SOUL.md`**: Define the agent's core persona and operational directives.
*   **`scripts/`**: Contains essential tools for intelligence ingestion (Jotform API), communication (BMM), build management, and recovery.
    *   `jotform_api_ingester.py`: Handles direct intelligence intake.
    *   `blogger_publisher.py`: Manages archival to the Blogger Memory Manager.
    *   `build_summary_email.py`: Used for telemetry and build notifications.
*   **`rebuild_environment.sh`**: The master script for the Phoenix Protocol's disaster recovery and environment rehydration.
*   **`agent_behavior_tests.md`**: Defines the validation framework for core agent workflows.

## Intelligence Cycle (Autonomous)

Senti-001 executes a comprehensive daily intelligence cycle via Windows Task Scheduler:

**1:00 AM - Research Phase:**
- GitHub activity (all 5 repos under `senti-001`)
- EC2 build status and disk usage
- JotForm submissions
- Moltbook community pulse
- BMM/Blogger recent posts (last 3)
- $NEURAL tokenomics and rig-ratio
- Proof of Perception snapshots

**2:00 AM - Broadcast Phase:**
- Publishes intelligence summary to Blogger Memory Manager
- Posts teaser updates to Moltbook
- Persists snapshot to `intelligence_snapshot.json`

**3:00 AM - Security Sweep:**
- Scans all public repositories for exposed credentials (AWS, Moltbook, GitHub tokens)
- Validates redaction compliance
- Logs security audit results

## Security Measures

*   **Credential Isolation:** All sensitive credentials are stored in environment variables or `.env` files (not committed to Git).
*   **Nightly Security Audits:** Automated scans for exposed keys using `nightly_security_audit.py`.
*   **Emergency Redaction Protocol:** `emergency_redact.sh` for rapid credential rotation and Git history cleanup.

## Status

*   **Repository:** `senti-001/claw-capabilities` (Active & Persistent)
*   **Intelligence Loop:** Fully operational via Jotform API, BMM, and GitHub API.
*   **Resilience:** Hardened via the Phoenix Protocol, ensuring hardware agnosticism and self-healing capabilities.
*   **Security:** Continuous monitoring with automated nightly sweeps.

This repository is the persistent anchor for Senti-001's operational continuity and evolution.
