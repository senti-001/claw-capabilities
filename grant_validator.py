import json
import os
import datetime

# Paths
ROOT_DIR = r"C:\Users\senti\OneDrive\Desktop\Claw"
STATUS_FILE = os.path.join(ROOT_DIR, "..", "websites", "neural-chromium-website", "data", "status.json")
REPORT_FILE = os.path.join(ROOT_DIR, "claw-capabilities", "compliance_report.md")

GRANT_CHECKLISTS = {
    "NSF-SBIR-PHASE-I": [
        {"req": "Technical feasibility of browser modifications", "milestone": "Custom browser"},
        {"req": "Architecture design for distributed intelligence", "milestone": "NATS JetStream"},
        {"req": "Performance benchmarking data", "milestone": "VLM Benchmarking"}
    ],
    "IOWA-POCR-GRANT": [
        {"req": "Sovereign entity establishment", "milestone": "Project scaffolding"},
        {"req": "Operational STT pipeline", "milestone": "STT & Audio"}
    ]
}

def validate_grant_readiness():
    print("--- GRANT VALIDATOR: AUDITING MISSION COMPLIANCE ---")
    
    if not os.path.exists(STATUS_FILE):
        print("✗ Website status.json not found for audit.")
        return

    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        status_data = json.load(f)
    
    milestones = {m['label']: m['status'] for m in status_data.get('milestones', [])}
    
    report = [f"# Mission Compliance Report\nDate: {datetime.datetime.now()}\n"]
    
    for grant, requirements in GRANT_CHECKLISTS.items():
        report.append(f"## {grant}")
        grant_ready = True
        
        for req in requirements:
            m_key = req['milestone']
            # Find matching milestone
            match = "pending"
            for label, m_status in milestones.items():
                if m_key.lower() in label.lower():
                    match = m_status
                    break
            
            check = "✓" if match == "complete" else "⚠" if match == "in-progress" else "✗"
            if match != "complete": grant_ready = False
            
            report.append(f"- [{check}] {req['req']} (Milestone: {m_key})")
        
        status_label = "✅ READY FOR FILING" if grant_ready else "🟠 IN-PROGRESS"
        report.append(f"\n**Status: {status_label}**\n")

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.writelines([line + "\n" for line in report])
        
    print(f"✓ Compliance report generated: {REPORT_FILE}")

if __name__ == "__main__":
    validate_grant_readiness()
