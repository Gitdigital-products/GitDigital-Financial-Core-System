# Repo folder tree (canonical layout)

`text
GitDigital-Financial-Core-System/
├─ dashboard.html
├─ dashboard.css
├─ loan-ledger.html
├─ loan-ledger.css
├─ credit-authority.html
├─ credit-authority.css
├─ badges.html
├─ badges.css
├─ audit-trail.html
├─ audit-trail.css
├─ document-vault.html
├─ document-vault.css
├─ promissory-note.html
├─ promissory-note.css
├─ kyc.html
├─ kyc.css
├─ collateral.html
├─ collateral.css
├─ forgiveness-addendum.html
├─ forgiveness-addendum.css
├─ credit-reporting.html
├─ credit-reporting.css
├─ governance.json
├─ sidebar.js
├─ README.md
├─ CONTRIBUTING.md
├─ badge-wall.md
├─ index.html
└─ .github/
   └─ workflows/
      └─ governance-check.yml
`

---

2. GitHub Actions: governance-check.yml

Basic CI that enforces structure + reminds reviewers of authority.

`yaml
name: Governance Check

on:
  pull_request:
    branches: [ main ]

jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Validate file structure
        run: |
          test -f governance.json
          test -f README.md
          test -f CONTRIBUTING.md

      - name: Ensure each HTML has matching CSS
        run: |
          for f in *.html; do
            base="${f%.html}"
            if [ ! -f "${base}.css" ] && [ "$base" != "index" ]; then
              echo "Missing CSS for $f"
              exit 1
            fi
          done

      - name: Warn on legal module changes without note
        run: |
          if git diff --name-only origin/main...HEAD | grep -E 'promissory-note|kyc|collateral|forgiveness-addendum|credit-reporting'; then
            echo "::warning::Legal modules changed. Ensure a Reviewer with proper badge signs off."
          fi
`

---

3. Tiny dynamic layer: audit-trail.js hook

Just enough to show this can go live later.

`javascript
// audit-trail.js
document.addEventListener("DOMContentLoaded", () => {
  const rows = document.querySelectorAll(".audit-table tbody tr");
  rows.forEach(r => r.classList.add("audit-row"));
});
`

Include on audit-trail.html:

`html
<script src="audit-trail.js"></script>
`

---

