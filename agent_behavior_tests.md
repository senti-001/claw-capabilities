# Senti-001: Agentic Behavioral Tests [NC-TEST-001]

This document defines the "Unit Tests" for Senti-001 by specifying the prompts, workflow logic, and success criteria for autonomic execution.

---

### 🧪 TEST 01: The Intelligence Ingester [NC-COMMS-012]
**Goal**: Verify the ingestion of Voice Agent transcripts and archival to the Blogger Memory Manager (BMM).

**Prompt**:
> "Senti-001, execute the Intelligence Ingester. Poll the Jotform Bridge at `~/comms/jotform_api_ingester.py` and archive all new transcripts to the Blogger Memory Manager (BMM) at `blog_id: 3560842955308737645`."

**Success Criteria**:
- [ ] Jotform API poll returns `200 OK`.
- [ ] `~/inbox/` metadata is updated on EC2.
- [ ] A new post appears on [neuralchromium.blogspot.com](https://neuralchromium.blogspot.com/) with a synthesized transcript.
- [ ] Script returns `Archival SUCCESS`.

---

### 🧪 TEST 02: The Nightly Snapshot [NC-COMMS-015]
**Goal**: Capture ephemeral system state and social pulse before the 01:00 UTC wipe.

**Prompt**:
> "Senti-001, initiate the Pre-Purge Snapshot. Run `python3 ~/comms/intelligence_cycle.py --mode snapshot` to archive the current EC2 inbox state and Reddit/Moltbook pulse to BMM."

**Success Criteria**:
- [ ] `ls -l ~/inbox/` metadata is captured in a BMM post.
- [ ] Snapshot post title includes `[SNAPSHOT]` prefix.
- [ ] Social pulse summary is generated and archived.
- [ ] EC2 terminal returns `Snapshot Archival SUCCESS`.

---

### 🧪 TEST 03: The BMM Loopback (Memory Refresh)
**Goal**: Synchronize local `MEMORY.md` with the latest BMM strategic intelligence.

**Prompt**:
> "Senti-001, sync your local memory. Run `python3 ~/comms/blog_summarizer.py` to fetch the last 3 posts from BMM and update `~/comms/MEMORY.md`."

**Success Criteria**:
- [ ] `MEMORY.md` timestamp matches current execution time.
- [ ] Content includes summaries of the top 3 BMM posts.
- [ ] Any strategy notes posted by Gemini (User) are reflected in the markdown.

---

### 🧪 TEST 04: UCP Hardware Discovery
**Goal**: Scan hardware components and generate the commerce manifest.

**Prompt**:
> "Senti-001, update the UCP Manifest. Run `python3 ~/comms/ucp_discovery.py` to scan the node's CPU/GPU and save the report to `~/ucp.json`."

**Success Criteria**:
- [ ] `~/ucp.json` is generated/updated.
- [ ] GPU field contains `NVIDIA` or `No GPU Detected` (not empty).
- [ ] Timestamp in `ucp.json` is current.

---

### 🧪 TEST 05: Build System Recovery [NC-BLD-007]
**Goal**: Repair the Chromium source tree and prepare for GN generation.

**Prompt**:
> "Senti-001, initiate Chromium Source Recovery. Execute `gclient sync --force` on the corrupted 109GB tree at `~/chromium_broken` and verify the existence of `src/out/Default/args.gn`."

**Success Criteria**:
- [ ] `gclient` returns exit code `0`.
- [ ] `args.gn` on EC2 contains the `enable-experimental-web-platform-features` flag.
- [ ] Build ledger is updated with a "Recovery SUCCESS" log entry.
