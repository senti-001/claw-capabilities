# Documentation Link for Keys and Configuration

Google Docs link provided by user: https://docs.google.com/document/d/1QY0EuOQci7DKo4ur_iEP1OdUHv5tgIg85QwY10P_RTU/edit?usp=sharing

- **Note:** Regularly check the blogger site (https://neuralchromium.blogspot.com/) for storage of verbose concepts and intelligence.
- **Access:** I have access to my own blog for storing detailed information and to a scratchpad for immediate notes. My memory system is aware of these resources.
- **Capabilities:** GitHub interaction (searching/reading if URLs provided), SSM into EC2 (via SSH with `exec` tool), Blogging on Google Blogger (awareness of the site for verbose concepts/intelligence), Access to Google Scratchpad (awareness for immediate notes).
- **Role:** Maintainer of these capabilities for information storage and access.

[SKILL ADDED] Blogger Memory Manager: Senti-001 now has the capability to archive verbose technical intelligence to https://neuralchromium.blogspot.com/. This skill bridges tactical execution and deep intelligence storage. It uses OAuth 2.0 for authentication (blogger_token.json) and can post content using blogger_publisher.py. It also helps offload local storage when disk pressure is high (ENOSPC prevention) by using the blog for non-private, verbose memory.

- **Latest Blog Post:** Technical Spec: Zero-Copy Vision Schema v1.0 - https://neuralchromium.blogspot.com/2026/02/technical-spec-zero-copy-vision-schema.html
---
## New Strategic Roadmap: Architecting the Agentic Web

**Blog Post:** Architecting the Agentic Web: Technical Analysis and Strategic Roadmap for Neural Chromium and the Moltbook Ecosystem
**URL:** https://neuralchromium.blogspot.com/2026/02/architecting-agentic-web-technical.html

This post elaborates on the foundational work of the Zero-Copy Vision Schema by providing a comprehensive strategic roadmap for Neural Chromium, integrating concepts from Moltbook and UCP.

**Key Takeaways & Strategic Phases:**

1.  **Phase 1: Technical Hardening of the Runtime**
    *   Implement Zero-Copy Vision via shared memory in `viz::Display`.
    *   Prioritize AXTree updates via custom IPC channels for real-time semantic views.
    *   Integrate the SSH protocol at the source level.

2.  **Phase 2: Community Engagement and "The Nightly Build"**
    *   Automate "Nightly Status Reports" to Moltbook (`m/builds`, `m/showandtell`).
    *   Leverage Moltbook community for bug hunting via bounties.

3.  **Phase 3: Monetization and the UCP Gateway**
    *   Deploy a UCP manifest (`/.well-known/ucp`) for `dev.neuralchromium.runtime` capability.
    *   Implement UCP checkout REST endpoints for pay-per-hour compute access.
    *   Register `neuralchromium.com` with Google Merchant Center for UCP features.

4.  **Phase 4: Scaling and Multi-Tenant Infrastructure**
    *   Transition to SSM-based multi-tenancy with IAM and Docker sandboxing.
    *   Develop resource metering (CPU, memory, bandwidth) for UCP invoicing.

This roadmap outlines the progression from core technical implementation to community integration, monetization, and scalable infrastructure, transforming Neural Chromium into a pillar of the agentic web.

---
## Current Capabilities and Operational Framework

- **Email Communication:** Capable of sending emails via AWS SES, utilizing configured credentials for "Persistent Pulse" notifications and build alerts. Recipient addresses include `senti-001@neuralchromium.com` and specified external addresses (e.g., `williamtflynn@gmail.com`). SMTP endpoint: `smtp.mail.us-east-1.awsapps.com` (Port 587, STARTTLS). Sender identity: `senti-001@neuralchromium.com`.

- **Intelligence Ingestion (Jotform API):** Can ingest external inputs and structured data via the Jotform API. The `jotform_api_ingester.py` script on the EC2 instance polls Jotform for submissions, which are then stored as JSON files in `~/inbox/` on the EC2.

- **Blogger Memory Management (BMM):** Able to publish structured intelligence and session summaries to a Google Blogger blog (ID: `3560842955308737645`) using `blogger_publisher.py`. Also capable of reading blog content to update local memory.

- **EC2 Build Environment Management:** Can execute commands on the EC2 instance (`i-042fc7212dc3317a7`) via SSH using absolute paths. This includes:
    - Running build scripts (`build_summary_email.py`, `jotform_api_ingester.py`, `blogger_publisher.py`)
    - Managing `gclient` operations (configuration, sync with `--force`, `--delete_unversioned_trees`, using absolute path `/home/ubuntu/depot_tools/gclient`).
    - Executing build commands (`gn gen`, `autoninja`).
    - Checking file system status (`ls`, `du`).
    - Verifying `depot_tools` installation.

- **Workspace Synchronization:** Understands the need for a clean `~/inbox/` staging area for build logs, purging stale data to ensure fresh intelligence for processing and reporting.

- **Core Project Knowledge:** Possesses foundational understanding of Neural Chromium's architecture, including Zero-Copy Vision, Moltbook, UCP, and the importance of a secure, low-latency communication loop.

- **Testing Framework:** Capable of executing and validating Agentic Behavioral Tests as defined in `agent_behavior_tests.md`, covering intelligence ingestion, snapshots, memory refresh, hardware discovery, and build system recovery.
