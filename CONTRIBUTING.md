# CONTRIBUTING.md (Reviewer‑Grade Contributor Rules)
This sets the tone for how contributors interact with the repo, how governance works, and how badge authority is enforced.

`markdown

Contributing to GitDigital Financial Core System

Welcome to the GitDigital Financial Core System.  
This repository implements the authoritative governance, ledger, and legal‑packet engine for the GitDigital ecosystem.

🔐 Governance Principles
All contributions must respect the following:

- Ledger Integrity — No modification to ledger logic without reviewer approval.
- Authority Separation — Only badge‑authorized contributors may modify credit‑authority modules.
- Legal Packet Consistency — Courthouse‑theme documents must maintain formatting, watermark, and signature‑block standards.
- Auditability — All changes must be traceable, documented, and reviewer‑stamped.

🏅 Badge‑Based Permissions
| Badge | Permissions |
|-------|-------------|
| Founder | Full authority across all modules |
| Reviewer | Approve PRs, stamp legal docs, modify ledger logic |
| Governance | Modify workflows, authority triggers, and audit logic |
| Compliance | Validate legal packet formatting and KYC flow |
| Contributor | Submit PRs for non‑governance modules |

📁 Repo Structure Rules
- Each HTML page must have its own CSS file.
- Dark‑theme pages use icons + fixed sidebar.
- Courthouse pages use text‑only + scrollable sidebar.
- All legal documents must include:
  - Serif headings  
  - Sans‑serif body  
  - Initial boxes  
  - Signature blocks  
  - Reviewer stamp  
  - GitDigital watermark  

🧪 Testing & Validation
Before submitting a PR:

1. Validate sidebar links across all pages.
2. Confirm courthouse pages render correctly on mobile.
3. Ensure badge wall displays all active badges.
4. Confirm audit‑trail entries follow timestamp format:
   YYYY‑MM‑DD HH:MM MST

📝 Pull Request Requirements
Every PR must include:

- Purpose of change  
- Affected modules  
- Reviewer badge required  
- Screenshots (if UI)  
- Audit‑trail entry (if governance‑related)

Thank you for helping maintain the integrity of the GitDigital ecosystem.
`

---

2. governance.json (Machine‑Readable Authority Schema)
This is the backbone for future automation, GitHub Actions, or the GitDigital Badge Authority App.

`json
{
  "version": "1.0.0",
  "modules": {
    "dashboard": { "theme": "dark", "authority": "contributor" },
    "loan_ledger": { "theme": "dark", "authority": "reviewer" },
    "credit_authority": { "theme": "dark", "authority": "governance" },
    "badges": { "theme": "dark", "authority": "contributor" },
    "promissory_note": { "theme": "courthouse", "authority": "reviewer" },
    "kyc": { "theme": "courthouse", "authority": "compliance" },
    "collateral": { "theme": "courthouse", "authority": "reviewer" },
    "forgiveness_addendum": { "theme": "courthouse", "authority": "reviewer" },
    "credit_reporting": { "theme": "courthouse", "authority": "reviewer" },
    "audit_trail": { "theme": "dark", "authority": "governance" },
    "document_vault": { "theme": "dark", "authority": "reviewer" }
  },
  "badges": {
    "founder": ["*"],
    "reviewer": ["loanledger", "promissorynote", "collateral", "forgivenessaddendum", "creditreporting", "document_vault"],
    "governance": ["creditauthority", "audittrail"],
    "compliance": ["kyc"],
    "contributor": ["dashboard", "badges"]
  }
}
`

This file is the source of truth for authority layers.

---

3. sidebar.js (Unified Navigation Logic)
This gives you a single JS file that handles:

- Active link highlighting  
- Theme switching (dark vs courthouse)  
- Scroll behavior for courthouse pages  
- Icon visibility rules  

`javascript
document.addEventListener("DOMContentLoaded", () => {
  const sidebarLinks = document.querySelectorAll(".sidebar nav a");
  const current = window.location.pathname.split("/").pop();

  sidebarLinks.forEach(link => {
    if (link.getAttribute("href") === current) {
      link.classList.add("active");
    }
  });

  // Theme detection
  const isCourthouse = document.body.classList.contains("courthouse");
  if (isCourthouse) {
    document.querySelectorAll(".icon").forEach(i => i.style.display = "none");
  }
});
`

You can drop this into /sidebar.js and include it on every page.

---

4. badge-wall.md (Documentation for the Badge System)
This explains the badge wall for contributors and reviewers.

`markdown

GitDigital Badge Wall

The Badge Wall is the visual and functional representation of authority within the GitDigital ecosystem.

🎖 Badge Categories

Founder
- Full authority across all modules  
- Can issue, revoke, or modify badges  

Reviewer
- Approves PRs  
- Stamps legal documents  
- Executes ledger and credit actions  

Governance
- Manages workflows  
- Controls authority triggers  
- Oversees audit‑trail integrity  

Compliance
- Validates KYC and legal packet formatting  
- Ensures courthouse‑theme consistency  

Contributor
- Can submit PRs  
- Can modify non‑governance modules  

📊 Badge Wall Locations
- /badges.html  
- /document-vault.html  
- /audit-trail.html  

Badges are not decorative — they are authority gates.
`

---

5. GitHub Pages Landing Page (index.html)
This gives the repo a public‑facing homepage if you enable GitHub Pages.

`html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>GitDigital Financial Core System</title>
  <style>
    body { background:#0f1115; color:#e6e6e6; font-family:Arial; padding:40px; }
    h1 { color:#2ee6c8; }
    a { color:#2ee6c8; text-decoration:none; }
  </style>
</head>
<body>
  <h1>GitDigital Financial Core System</h1>
  <p>The authoritative governance, ledger, and legal‑packet engine for the GitDigital ecosystem.</p>

  <h2>Repository</h2>
  <p><a href="https://github.com/Gitdigital-products/GitDigital-Financial-Core-System">View on GitHub</a></p>

  <h2>Modules</h2>
  <ul>
    <li>Dashboard</li>
    <li>Loan Ledger</li>
    <li>Credit Authority</li>
    <li>Badge Console</li>
    <li>Audit Trail</li>
    <li>Document Vault</li>
    <li>Promissory Note</li>
    <li>KYC Intake</li>
    <li>Collateral Statement</li>
    <li>Forgiveness Addendum</li>
    <li>Credit Reporting</li>
  </ul>
</body>
</html>
`

---

