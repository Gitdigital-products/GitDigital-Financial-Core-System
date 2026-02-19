async function syncPromissoryNote() {
  const ledger = await fetch("data/ledger.json").then(r => r.json());
  const principal = ledger.entries.find(e => e.type === "Principal Issued");

  document.getElementById("principal-amount").innerText =
    `$${principal.amount}`;
}
