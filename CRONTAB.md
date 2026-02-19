# Mission CRONTAB Manifest [NC-CRON-001]

This manifest tracks all mission-critical scheduled tasks and persistent processes for project Neural Chromium.

## 🕒 Scheduled Tasks (Windows Task Scheduler)

| Task Name | Trigger | Command / Script | Purpose |
| :--- | :--- | :--- | :--- |
| `Senti-Investor-Audit` | 10:30 AM Daily | `nightly_investor_audit.py` | Syncs intelligence pool with dashboard metrics. |
| `Senti-001-Intelligence-Cycle` | Every 6 Hours | `intelligence_cycle.py --mode full` | Broadcasts advancements to BMM/Blog. |
| `Senti_001_Ingest` | Every 1 Hour | `jotform_sota_ingester.py` | (Legacy) Ingests form data into intelligence pool. |

## 🔄 Persistent Processes (Manual/Background)

| Process Name | Mode | Script | Purpose |
| :--- | :--- | :--- | :--- |
| `Senti-001-Agent` | Background | `jotform_conversational_agent.py` | High-availability conversational response bridge. |
| `Next.js Dev Server` | Manual | `npm run dev` | Local development and verification environment. |

## 🛠️ Management Directive

- **Editing**: All task modifications should be performed via `manage-tasks.py` to ensure consistency.
- **Logging**: All tasks append output to `c:\Users\senti\OneDrive\Desktop\Claw\logs\task_logs.jsonl`.
- **Health Checks**: Senti-001 performs a nightly audit and reports failures via the `Sovereign Concierge`.
