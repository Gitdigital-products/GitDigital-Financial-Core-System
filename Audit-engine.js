async function logAudit({ actor, module, action }) {
  const timestamp = new Date().toISOString();

  console.log(`[AUDIT] ${timestamp} | ${actor} | ${module} | ${action}`);
}
