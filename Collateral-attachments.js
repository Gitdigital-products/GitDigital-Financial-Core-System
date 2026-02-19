fetch("collateral-attachments.json")
  .then(r => r.json())
  .then(data => {
    const list = document.getElementById("collateral-files");
    data.collateral_files.forEach(file => {
      const li = document.createElement("li");
      li.textContent = `${file.filename} (ref: ${file.storage_ref})`;
      list.appendChild(li);
    });
  });
