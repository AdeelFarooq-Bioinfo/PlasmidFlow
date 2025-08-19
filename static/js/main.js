// PlasmidFlow front-end logic using Fetch/Axios + Plotly.js
const TRAITS = ["ARGs", "Virulence", "T4SS", "MGEs"];
let datasetId = null;
let lastFigure = null;

// Render trait checkboxes
function renderTraitCheckboxes(containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  TRAITS.forEach(t => {
    const id = `${containerId}-${t}`;
    const div = document.createElement("div");
    div.className = "form-check";
    div.innerHTML = `
      <input class="form-check-input" type="checkbox" value="${t}" id="${id}">
      <label class="form-check-label" for="${id}">${t}</label>
    `;
    container.appendChild(div);
  });
}

["sankeyTraits", "networkTraits", "heatmapTraits"].forEach(renderTraitCheckboxes);

// Controls
function currentStyle() {
  return {
    node_color: document.getElementById("styleNodeColor").value || "red",
    edge_color: document.getElementById("styleEdgeColor").value || "skyblue",
    node_size: parseInt(document.getElementById("styleNodeSize").value || "12"),
    bg_color: document.getElementById("styleBgColor").value || "white",
    font_size: parseInt(document.getElementById("styleFontSize").value || "14")
  };
}

function currentFigType() {
  if (document.getElementById("figSankey").checked) return "sankey";
  if (document.getElementById("figNetwork").checked) return "network";
  return "heatmap";
}

function selectedTraits(containerId) {
  const checks = document.querySelectorAll(`#${containerId} input[type=checkbox]:checked`);
  return Array.from(checks).map(c => c.value);
}

function setStatus(txt) {
  document.getElementById("statusText").innerText = txt;
}

async function refreshFigure() {
  if (!datasetId) {
    setStatus("Upload a dataset to start");
    return;
  }
  const envFilter = document.getElementById("envFilter").value || "";
  const ftype = currentFigType();
  const traits = ftype === "sankey" ? selectedTraits("sankeyTraits")
                : ftype === "network" ? selectedTraits("networkTraits")
                : selectedTraits("heatmapTraits");
  const scale = document.getElementById("heatmapScale").value;

  const payload = {
    dataset_id: datasetId,
    env_filter: envFilter,
    traits: traits,
    style: currentStyle(),
    scale: scale
  };

  try {
    setStatus("Rendering...");
    const { data } = await axios.post(`/api/figure/${ftype}`, payload);
    lastFigure = data;
    Plotly.react("plotArea", data.data, data.layout, {responsive: true});
    setStatus("Done");
  } catch (err) {
    console.error(err);
    setStatus("Error rendering figure");
    const msg = err?.response?.data?.error || err?.message || "Unknown error";
    Plotly.purge("plotArea");
    document.getElementById("plotArea").innerHTML = `<div class="text-danger">❌ ${msg}</div>`;
  }
}

async function doExport() {
  if (!lastFigure) {
    alert("No figure to export yet.");
    return;
  }
  const fmt = document.getElementById("exportFormat").value;
  setStatus(`Exporting ${fmt.toUpperCase()}...`);
  try {
    const resp = await fetch("/api/export", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ figure: lastFigure, format: fmt, width: 1200, height: 800, scale: 2 })
    });
    if (!resp.ok) {
      const e = await resp.json().catch(()=>({error:"Export failed"}));
      throw new Error(e.error || "Export failed");
    }
    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `plasmidflow.${fmt}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setStatus("Exported");
  } catch (e) {
    console.error(e);
    setStatus("Export error");
    alert("Export failed: " + e.message);
  }
}

function saveStyleJson() {
  const style = currentStyle();
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(style, null, 2));
  const a = document.createElement("a");
  a.href = dataStr;
  a.download = "plasmidflow_style.json";
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function loadStyleFromFile() {
  const input = document.getElementById("inputStyleFile");
  if (!input.files || !input.files[0]) {
    alert("Select a JSON file first.");
    return;
  }
  const file = input.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const style = JSON.parse(reader.result);
      if (style.node_color) document.getElementById("styleNodeColor").value = style.node_color;
      if (style.edge_color) document.getElementById("styleEdgeColor").value = style.edge_color;
      if (style.node_size) document.getElementById("styleNodeSize").value = style.node_size;
      if (style.bg_color) document.getElementById("styleBgColor").value = style.bg_color;
      if (style.font_size) document.getElementById("styleFontSize").value = style.font_size;
      refreshFigure();
    } catch (e) {
      alert("Invalid JSON style file.");
    }
  };
  reader.readAsText(file);
}

// Upload handler
document.getElementById("csvFile").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const form = new FormData();
  form.append("file", file);
  document.getElementById("previewArea").innerHTML = "<em>Uploading...</em>";
  try {
    const resp = await fetch("/api/upload", { method: "POST", body: form });
    const out = await resp.json();
    if (!resp.ok) {
      throw new Error(out.error || "Upload failed");
    }
    datasetId = out.dataset_id;
    const pv = out.preview;
    // Render preview table
    const tbl = document.createElement("table");
    tbl.className = "table table-sm table-striped";
    const thead = document.createElement("thead");
    const trh = document.createElement("tr");
    pv.columns.forEach(c => {
      const th = document.createElement("th"); th.textContent = c; trh.appendChild(th);
    });
    thead.appendChild(trh);
    tbl.appendChild(thead);
    const tb = document.createElement("tbody");
    pv.rows.forEach(r => {
      const tr = document.createElement("tr");
      pv.columns.forEach(c => {
        const td = document.createElement("td");
        td.textContent = r[c];
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    tbl.appendChild(tb);
    document.getElementById("previewArea").innerHTML = "";
    document.getElementById("previewArea").appendChild(tbl);
    document.getElementById("previewArea").insertAdjacentHTML("beforeend", `<div class="small text-muted">Showing ${pv.rows.length} of ${pv.n_total} rows.</div>`);
    refreshFigure();
  } catch (err) {
    document.getElementById("previewArea").innerHTML = `<div class="text-danger">❌ ${err.message}</div>`;
  }
});

// Debounced inputs
let debTimer = null;
["envFilter", "styleNodeColor", "styleEdgeColor", "styleNodeSize", "styleBgColor", "styleFontSize", "heatmapScale"].forEach(id => {
  const el = document.getElementById(id);
  if (el) {
    el.addEventListener("input", () => {
      if (debTimer) clearTimeout(debTimer);
      debTimer = setTimeout(refreshFigure, 300);
    });
  }
});

// Trait checkboxes change listeners
["sankeyTraits", "networkTraits", "heatmapTraits"].forEach(cid => {
  document.getElementById(cid).addEventListener("change", refreshFigure);
});

// Figure type toggles
["figSankey", "figNetwork", "figHeatmap"].forEach(id => {
  document.getElementById(id).addEventListener("change", refreshFigure);
});

// Export and Style
document.getElementById("btnExport").addEventListener("click", doExport);
document.getElementById("btnSaveStyle").addEventListener("click", saveStyleJson);
document.getElementById("btnUploadStyle").addEventListener("click", loadStyleFromFile);

// Initial render
refreshFigure();