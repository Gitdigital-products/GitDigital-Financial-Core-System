// authority-engine.js

async function loadGovernance() {
  const res = await fetch("governance.json");
  return await res.json();
}

async function hasAuthority(userBadge, moduleName) {
  const gov = await loadGovernance();

  // Founder bypass
  if (userBadge === "founder") return true;

  const allowedModules = gov.badges[userBadge] || [];
  return allowedModules.includes(moduleName);
}

async function executeAction({ userBadge, module, action, payload }) {
  const allowed = await hasAuthority(userBadge, module);

  if (!allowed) {
    return {
      success: false,
      message: `User with badge '${userBadge}' is not authorized to perform '${action}' on '${module}'.`
    };
  }

  // Ledger mutation example
  if (module === "loan_ledger" && action === "addEntry") {
    const ledger = await fetch("data/ledger.json").then(r => r.json());
    ledger.entries.push(payload);

    return {
      success: true,
      message: "Ledger entry added.",
      updatedLedger: ledger
    };
  }

  // Credit authority example
  if (module === "credit_authority" && action === "executeForgiveness") {
    return {
      success: true,
      message: "Forgiveness executed.",
      forgiveness: payload
    };
  }

  return {
    success: true,
    message: `Action '${action}' executed on module '${module}'.`
  };
}
