/* ============================================================
   MetroLine frontend
   The list lives in Python; this file only paints what the API
   returns. It never reorders the list on its own.
   ============================================================ */

let lineData = null;        // last state received from the API
let backwardData = null;    // cached tail -> head traversal
let selectedName = null;    // station shown in the memory view
let activeTab = "forward";
let pendingAdded = null;    // station to animate as "just added"
let pendingRemoved = null;  // station to animate as "just removed"

/* ---------------- API helpers ---------------- */

async function apiGet(path) {
  const response = await fetch(path);
  const data = await response.json();
  if (!data.ok) {
    showToast(data.message, true);
  }
  return data;
}

async function apiSend(method, path, body) {
  const options = { method: method };
  if (body !== undefined) {
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(body);
  }
  const response = await fetch(path, options);
  const data = await response.json();
  showToast(data.message, !data.ok);
  return data;
}

async function refresh() {
  const data = await apiGet("/api/line");
  if (data.ok) {
    lineData = data.line;
    backwardData = null;           // the server changed: cache is stale
    if (selectedName === null || findStation(selectedName) === null) {
      selectedName = lineData.current;   // fall back to the train position
    }
    renderLine();
  }
}

/* ---------------- small helpers ---------------- */

function findStation(name) {
  if (lineData === null || name === null) {
    return null;
  }
  for (const station of lineData.stations) {
    if (station.name === name) {
      return station;
    }
  }
  return null;
}

function currentStation() {
  return findStation(lineData.current);
}

function showToast(message, isError) {
  const box = document.getElementById("toasts");
  const toast = document.createElement("div");
  toast.className = "toast" + (isError ? " toast-error" : "");
  toast.textContent = message;
  box.appendChild(toast);
  setTimeout(function () {
    toast.remove();
  }, 3200);
}

function sleep(ms) {
  return new Promise(function (resolve) {
    setTimeout(resolve, ms);
  });
}

/* ---------------- rendering ---------------- */

function renderLine() {
  const empty = lineData.size === 0;
  document.getElementById("stationCount").textContent = lineData.size;
  document.getElementById("emptyState").hidden = !empty;

  renderTrack();
  renderStationList();
  renderSelects();
  renderControls();
  renderMemoryView();
  renderTraversal();
}

function renderTrack() {
  const track = document.getElementById("lineTrack");
  track.innerHTML = "";

  lineData.stations.forEach(function (station, index) {
    if (index > 0) {
      track.appendChild(buildArrows());
    }
    track.appendChild(buildStation(station));
  });

  if (pendingAdded !== null) {
    const added = track.querySelector('[data-name="' + cssEscape(pendingAdded) + '"]');
    if (added) {
      added.classList.add("just-added");
      added.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    }
    pendingAdded = null;
  }
}

function cssEscape(value) {
  return value.replace(/["\\]/g, "\\$&");
}

function buildStation(station) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "station";
  button.dataset.name = station.name;
  if (station.is_current) {
    button.classList.add("is-current");
  }
  if (pendingRemoved === station.name) {
    button.classList.add("just-removed");
  }

  if (station.is_current) {
    const train = document.createElement("span");
    train.className = "station-train";
    train.setAttribute("aria-hidden", "true");
    train.textContent = "\u{1F686}";   // train locomotive emoji
    button.appendChild(train);
  }

  const dot = document.createElement("span");
  dot.className = "station-dot";
  dot.textContent = station.index + 1;
  button.appendChild(dot);

  const name = document.createElement("span");
  name.className = "station-name";
  name.textContent = station.name;
  button.appendChild(name);

  const zone = document.createElement("span");
  zone.className = "station-zone";
  zone.textContent = "zone " + station.zone;
  button.appendChild(zone);

  button.addEventListener("mouseenter", function () {
    selectedName = station.name;
    renderMemoryView();
  });
  button.addEventListener("click", function () {
    selectedName = station.name;
    renderMemoryView();
  });

  return button;
}

function buildArrows() {
  const arrows = document.createElement("div");
  arrows.className = "link-arrows";
  arrows.setAttribute("aria-hidden", "true");

  const next = document.createElement("span");
  next.className = "arrow-next";
  next.textContent = "→ next";
  arrows.appendChild(next);

  const prev = document.createElement("span");
  prev.className = "arrow-prev";
  prev.textContent = "← prev";
  arrows.appendChild(prev);

  return arrows;
}

function renderStationList() {
  const list = document.getElementById("stationList");
  list.innerHTML = "";

  lineData.stations.forEach(function (station) {
    const item = document.createElement("li");

    const name = document.createElement("span");
    name.className = "list-name";
    name.textContent = station.name;
    item.appendChild(name);

    const zone = document.createElement("span");
    zone.className = "list-zone";
    zone.textContent = "z" + station.zone;
    item.appendChild(zone);

    if (station.is_current) {
      const badge = document.createElement("span");
      badge.className = "list-current";
      badge.textContent = "train";
      item.appendChild(badge);
    }

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "btn-delete";
    remove.textContent = "✕";
    remove.setAttribute("aria-label", "Remove station " + station.name);
    remove.addEventListener("click", function () {
      removeStation(station.name);
    });
    item.appendChild(remove);

    list.appendChild(item);
  });
}

function renderSelects() {
  const goto = document.getElementById("gotoSelect");
  const after = document.getElementById("afterSelect");
  const gotoValue = goto.value;
  const afterValue = after.value;

  goto.innerHTML = '<option value="">Select a station</option>';
  after.innerHTML = '<option value="">Select a station</option>';

  lineData.stations.forEach(function (station) {
    const optionGoto = document.createElement("option");
    optionGoto.value = station.name;
    optionGoto.textContent = station.name;
    goto.appendChild(optionGoto);

    const optionAfter = document.createElement("option");
    optionAfter.value = station.name;
    optionAfter.textContent = station.name;
    after.appendChild(optionAfter);
  });

  goto.value = findStation(gotoValue) ? gotoValue : "";
  after.value = findStation(afterValue) ? afterValue : "";
}

function renderControls() {
  const station = currentStation();
  const atHead = station === null || station.prev_name === null;
  const atTail = station === null || station.next_name === null;
  const empty = lineData.size === 0;

  document.getElementById("btnPrevious").disabled = empty || atHead;
  document.getElementById("btnNext").disabled = empty || atTail;
  document.getElementById("btnReverse").disabled = empty;
  document.getElementById("gotoSelect").disabled = empty;
}

function renderMemoryView() {
  const station = findStation(selectedName);

  const prevChip = document.getElementById("prevChip");
  const nextChip = document.getElementById("nextChip");
  const dataChip = document.getElementById("dataChip");

  if (station === null) {
    prevChip.textContent = "← None";
    prevChip.className = "chip chip-none";
    prevChip.disabled = true;
    nextChip.textContent = "None →";
    nextChip.className = "chip chip-none";
    nextChip.disabled = true;
    dataChip.textContent = "No station selected";
  } else {
    // prev pointer
    if (station.prev_name === null) {
      prevChip.textContent = "← None";
      prevChip.className = "chip chip-none";
      prevChip.disabled = true;
    } else {
      prevChip.textContent = "← " + station.prev_name;
      prevChip.className = "chip chip-prev";
      prevChip.disabled = false;
      prevChip.onclick = function () {
        selectedName = station.prev_name;
        renderMemoryView();
        highlightInLine();
      };
    }

    dataChip.textContent = station.name + " · zone " + station.zone;

    // next pointer
    if (station.next_name === null) {
      nextChip.textContent = "None →";
      nextChip.className = "chip chip-none";
      nextChip.disabled = true;
    } else {
      nextChip.textContent = station.next_name + " →";
      nextChip.className = "chip chip-next";
      nextChip.disabled = false;
      nextChip.onclick = function () {
        selectedName = station.next_name;
        renderMemoryView();
        highlightInLine();
      };
    }
  }

  document.getElementById("metaHead").textContent = lineData.head || "—";
  document.getElementById("metaTail").textContent = lineData.tail || "—";
  document.getElementById("metaSize").textContent = lineData.size;
}

function highlightInLine() {
  const element = document.querySelector(
    '#lineTrack [data-name="' + cssEscape(selectedName) + '"]'
  );
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  }
}

async function renderTraversal() {
  const box = document.getElementById("traversal");
  box.innerHTML = "";

  let stations;
  if (activeTab === "forward") {
    stations = lineData.stations;
  } else {
    if (backwardData === null) {
      const data = await apiGet("/api/line/backward");
      if (!data.ok) {
        return;
      }
      backwardData = data.backward;
    }
    stations = backwardData;
  }

  if (stations.length === 0) {
    const empty = document.createElement("span");
    empty.className = "chip chip-none";
    empty.textContent = "empty list";
    box.appendChild(empty);
    return;
  }

  stations.forEach(function (station) {
    const chip = document.createElement("span");
    chip.className = "chip";
    if (station.is_current) {
      chip.classList.add("current-chip");
    }
    if (station.name === lineData.head) {
      chip.classList.add("head-chip");
    }
    if (station.name === lineData.tail) {
      chip.classList.add("tail-chip");
    }
    chip.textContent = station.name;
    box.appendChild(chip);
  });
}

/* ---------------- actions ---------------- */

async function moveTrain(path) {
  const data = await apiSend("POST", path);
  if (data.ok) {
    selectedName = data.line.current;
    await refresh();
    highlightInLine();
  }
}

async function removeStation(name) {
  const confirmed = window.confirm('Remove station "' + name + '"?');
  if (!confirmed) {
    return;
  }
  pendingRemoved = name;
  renderTrack();
  await sleep(350);
  const data = await apiSend("DELETE", "/api/stations/" + encodeURIComponent(name));
  pendingRemoved = null;
  if (data.ok) {
    if (selectedName === name) {
      selectedName = null;
    }
    await refresh();
  } else {
    renderLine();
  }
}

async function addStation(event) {
  event.preventDefault();
  const name = document.getElementById("stationName").value.trim();
  const zone = document.getElementById("stationZone").value;
  const position = document.getElementById("stationPosition").value;

  const body = { name: name, zone: Number(zone), position: position };
  if (position === "after") {
    body.after = document.getElementById("afterSelect").value;
    if (body.after === "") {
      showToast("Choose the station to insert after", true);
      return;
    }
  }

  const data = await apiSend("POST", "/api/stations", body);
  if (data.ok) {
    pendingAdded = name;
    selectedName = name;
    document.getElementById("stationName").value = "";
    await refresh();
  }
}

async function searchStation(event) {
  event.preventDefault();
  const name = document.getElementById("searchName").value.trim();
  if (name === "") {
    showToast("Type a station name to search", true);
    return;
  }
  const data = await apiGet("/api/stations/search?name=" + encodeURIComponent(name));
  if (data.ok) {
    selectedName = data.found.name;
    renderMemoryView();
    highlightInLine();
    showToast(data.message, false);
  }
}

async function reverseLine() {
  const track = document.getElementById("lineTrack");
  track.classList.add("flipping");
  await sleep(500);
  const data = await apiSend("POST", "/api/line/reverse");
  track.classList.remove("flipping");
  if (data.ok) {
    await refresh();
  }
}

/* ---------------- wiring ---------------- */

function wireEvents() {
  document.getElementById("btnPrevious").addEventListener("click", function () {
    moveTrain("/api/train/previous");
  });
  document.getElementById("btnNext").addEventListener("click", function () {
    moveTrain("/api/train/next");
  });
  document.getElementById("btnReverse").addEventListener("click", reverseLine);

  document.getElementById("gotoSelect").addEventListener("change", function (event) {
    const name = event.target.value;
    if (name !== "") {
      moveTrainWithBody("/api/train/goto", { name: name });
    }
  });

  document.getElementById("addForm").addEventListener("submit", addStation);
  document.getElementById("searchForm").addEventListener("submit", searchStation);

  document.getElementById("stationPosition").addEventListener("change", function (event) {
    document.getElementById("afterField").hidden = event.target.value !== "after";
  });

  document.getElementById("tabForward").addEventListener("click", function () {
    activeTab = "forward";
    document.getElementById("tabForward").classList.add("active");
    document.getElementById("tabForward").setAttribute("aria-selected", "true");
    document.getElementById("tabBackward").classList.remove("active");
    document.getElementById("tabBackward").setAttribute("aria-selected", "false");
    renderTraversal();
  });

  document.getElementById("tabBackward").addEventListener("click", function () {
    activeTab = "backward";
    document.getElementById("tabBackward").classList.add("active");
    document.getElementById("tabBackward").setAttribute("aria-selected", "true");
    document.getElementById("tabForward").classList.remove("active");
    document.getElementById("tabForward").setAttribute("aria-selected", "false");
    renderTraversal();
  });
}

async function moveTrainWithBody(path, body) {
  const data = await apiSend("POST", path, body);
  if (data.ok) {
    selectedName = data.line.current;
    await refresh();
    highlightInLine();
  }
}

wireEvents();
refresh();
