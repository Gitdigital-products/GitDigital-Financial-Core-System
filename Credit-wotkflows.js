async function loadWorkflows() {
  const res = await fetch("credit-workflows.json");
  return await res.json();
}

async function runWorkflow(workflowId, context) {
  const { workflows } = await loadWorkflows();
  const wf = workflows.find(w => w.id === workflowId);
  if (!wf) {
    console.error("Workflow not found:", workflowId);
    return;
  }

  for (const step of wf.actions) {
    console.log(`Executing step: ${step}`);
    // Here you’d call into authority-engine, legal-sync, audit-engine, etc.
  }
}
