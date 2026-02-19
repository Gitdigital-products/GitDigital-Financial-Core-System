fetch("data/ledger.json")
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";

    data.entries.forEach(entry => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${entry.date}</td>
        <td>${entry.type}</td>
        <td>${entry.amount < 0 ? "-" : ""}$${Math.abs(entry.amount)}</td>
        <td>${entry.reviewer}</td>
      `;

      tbody.appendChild(row);
    });
  });
