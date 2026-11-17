/**
 * My FND Journey — Phase 0 visual interaction prototype.
 *
 * No learner-account API calls, symptom storage, analytics or cloud sync.
 * Changes persist as world coordinates in IndexedDB, and never imply an
 * activity was performed merely because its visual object was placed.
 */
import {
  WORLD, OBJECTS, emptyRoom, addObject, moveObject, bringToFront,
  removeObject, pointerToWorld, centeredZoomScroll
} from "./scene-model.mjs";
import { loadRoom, saveRoom, deleteRoom, deleteAllRooms } from "./storage.mjs";

const byId = id => document.getElementById(id);
const elements = {
  scene: byId("scene"), space: byId("scene-space"), viewport: byId("scene-viewport"),
  drawers: byId("drawers"), sceneList: byId("object-list"),
  status: byId("save-status"), helper: byId("placement-hint"),
  selection: byId("selection-status"), day: byId("room-date"),
  zoomValue: byId("zoom-value"), addCenter: byId("add-centre"),
  undo: byId("undo"), deleteDay: byId("delete-day"),
  deleteAll: byId("delete-all"), bringFront: byId("bring-front"),
  remove: byId("remove-selected"), controls: byId("selected-controls")
};

let room = emptyRoom(localDate(new Date()));
let zoom = 0.7;
let selectedId = null;
let armedType = null;
let drag = null;
let ready = false;
let pendingSave = Promise.resolve();
const undoStack = [];

/** Preserve local civil day, not the ISO UTC date which may be different. */
function localDate(date) {
  const pad = number => String(number).padStart(2, "0");
  return date.getFullYear() + "-" + pad(date.getMonth() + 1) + "-" + pad(date.getDate());
}

/** No user content is ever written with innerHTML. */
function make(tag, className, label) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (label !== undefined) node.textContent = label;
  return node;
}

function announce(message) {
  elements.helper.textContent = message;
}

/** Append a snapshot for undo, with bounded memory usage. */
function remember(previous) {
  undoStack.push(structuredClone(previous));
  if (undoStack.length > 30) undoStack.shift();
}

/**
 * Serialize IndexedDB writes to prevent two fast edits from being persisted
 * in reverse order. Take a snapshot before the asynchronous transaction.
 */
function queueSave() {
  const snapshot = structuredClone(room);
  elements.status.textContent = "Saving on this device…";
  pendingSave = pendingSave.catch(() => {}).then(() => saveRoom(snapshot));
  pendingSave.then(() => {
    if (room.date === snapshot.date) elements.status.textContent = "Saved on this device";
  }).catch(() => {
    elements.status.textContent = "Could not save. Your edits may be lost on refresh.";
  });
}

/** Apply a user-visible edit atomically in the local view. */
function changeRoom(next) {
  if (!ready || next === room) return;
  remember(room);
  room = next;
  draw();
  queueSave();
}

/** Build an accessible activity drawer, kept small for the initial spike. */
function renderDrawers() {
  const grouped = new Map();
  for (const [id, item] of Object.entries(OBJECTS)) {
    if (!grouped.has(item.drawer)) grouped.set(item.drawer, []);
    grouped.get(item.drawer).push({ id, ...item });
  }
  for (const [drawerName, entries] of grouped.entries()) {
    const details = make("details", "drawer");
    details.open = true;
    details.append(make("summary", "", drawerName));
    const tray = make("div", "drawer-items");
    for (const item of entries) {
      const button = make("button", "drawer-item", item.symbol + " " + item.name);
      button.type = "button";
      button.dataset.type = item.id;
      button.addEventListener("click", () => {
        armedType = item.id;
        selectedId = null;
        elements.addCenter.disabled = false;
        announce(item.name + " selected. Tap the scene to place it, or use Add at centre.");
        draw();
      });
      tray.append(button);
    }
    details.append(tray);
    elements.drawers.append(details);
  }
}

/** Refresh the scene, accessible list, selected controls and drawer state. */
function draw() {
  elements.scene.replaceChildren();
  const ordered = [...room.objects].sort((a, b) => a.z - b.z);
  for (const object of ordered) {
    const info = OBJECTS[object.type];
    const button = make("button", "scene-object" + (object.id === selectedId ? " is-selected" : ""));
    button.type = "button";
    button.dataset.id = object.id;
    button.style.left = object.x + "px";
    button.style.top = object.y + "px";
    button.style.zIndex = String(object.z);
    button.style.width = info.width * object.scale + "px";
    button.style.height = info.height * object.scale + "px";
    button.setAttribute("aria-label", info.name + ", placed activity object. Use arrow keys to move.");
    const symbol = make("span", "object-symbol", info.symbol);
    symbol.setAttribute("aria-hidden", "true");
    button.append(symbol, make("span", "object-name", info.name));
    button.addEventListener("pointerdown", event => startDrag(event, object.id));
    // Keyboard activation selects just as touch does. Pointer selection is
    // handled on pointerup to avoid fighting with drag capture.
    button.addEventListener("click", event => {
      if (event.detail !== 0) return; // Synthetic keyboard click only.
      selectedId = object.id;
      armedType = null;
      draw();
      elements.selection.focus();
    });
    button.addEventListener("keydown", event => {
      const step = event.shiftKey ? 4 : 20;
      const offset = {
        ArrowLeft: [-step, 0], ArrowRight: [step, 0],
        ArrowUp: [0, -step], ArrowDown: [0, step]
      }[event.key];
      if (!offset) return;
      event.preventDefault();
      selectedId = object.id;
      changeRoom(moveObject(room, object.id, object.x + offset[0], object.y + offset[1]));
      elements.scene.querySelector('[data-id="' + object.id + '"]')?.focus();
    });
    elements.scene.append(button);
  }
  renderObjectList(ordered);

  for (const button of elements.drawers.querySelectorAll("[data-type]")) {
    const active = button.dataset.type === armedType;
    button.setAttribute("aria-pressed", String(active));
  }
  const selected = room.objects.find(o => o.id === selectedId);
  elements.selection.textContent = selected
    ? "Selected: " + OBJECTS[selected.type].name
    : "No object selected";
  elements.controls.hidden = !selected;
  elements.undo.disabled = undoStack.length === 0;
  elements.deleteDay.disabled = !room.objects.length;
  elements.deleteAll.disabled = !ready;
}

/** List selection never requires successfully touching an occluded sprite. */
function renderObjectList(ordered) {
  elements.sceneList.replaceChildren();
  if (!ordered.length) {
    const empty = make("li", "empty-hint", "This room is empty. Choose an object from a drawer.");
    elements.sceneList.append(empty);
    return;
  }
  for (const object of [...ordered].reverse()) {
    const item = make("li", "list-object");
    const label = make("span", "list-label", OBJECTS[object.type].symbol + " " + OBJECTS[object.type].name);
    item.append(label);
    const select = make("button", "small", "Select");
    select.type = "button";
    select.addEventListener("click", () => {
      selectedId = object.id;
      armedType = null;
      draw();
      elements.selection.focus();
    });
    const locate = make("button", "small", "Locate");
    locate.type = "button";
    locate.addEventListener("click", () => locateObject(object.id));
    item.append(select, locate);
    elements.sceneList.append(item);
  }
}

/**
 * Scroll to the object rather than changing saved coordinates. If the object
 * is fully hidden by another, select it from the list and bring it forward.
 */
function locateObject(id) {
  const item = room.objects.find(o => o.id === id);
  if (!item) return;
  selectedId = id;
  armedType = null;
  draw();
  const target = elements.scene.querySelector('[data-id="' + id + '"]');
  if (!target) return;
  const x = (item.x + OBJECTS[item.type].width * item.scale / 2) * zoom;
  const y = (item.y + OBJECTS[item.type].height * item.scale / 2) * zoom;
  elements.viewport.scrollLeft = Math.max(0, x - elements.viewport.clientWidth / 2);
  elements.viewport.scrollTop = Math.max(0, y - elements.viewport.clientHeight / 2);
  target.focus({ preventScroll: true });
  announce("Located " + OBJECTS[item.type].name + ". Use Bring to front if it is covered.");
}

/** Update only position while dragging, retaining pointer capture and focus. */
function startDrag(event, id) {
  if (!ready || event.button !== 0) return;
  event.preventDefault();
  const target = event.currentTarget;
  const item = room.objects.find(o => o.id === id);
  if (!item) return;
  armedType = null;
  drag = {
    id, pointerId: event.pointerId, clientX: event.clientX, clientY: event.clientY,
    originalX: item.x, originalY: item.y, previous: structuredClone(room), moved: false
  };
  target.setPointerCapture(event.pointerId);
  target.addEventListener("pointermove", onDragMove);
  target.addEventListener("pointerup", finishDrag);
  target.addEventListener("pointercancel", cancelDrag);
}

function onDragMove(event) {
  if (!drag || event.pointerId !== drag.pointerId) return;
  const dx = (event.clientX - drag.clientX) / zoom;
  const dy = (event.clientY - drag.clientY) / zoom;
  if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
  const next = moveObject(room, drag.id, drag.originalX + dx, drag.originalY + dy);
  room = next;
  const item = room.objects.find(o => o.id === drag.id);
  event.currentTarget.style.left = item.x + "px";
  event.currentTarget.style.top = item.y + "px";
}

function detachDrag(target) {
  target.removeEventListener("pointermove", onDragMove);
  target.removeEventListener("pointerup", finishDrag);
  target.removeEventListener("pointercancel", cancelDrag);
  drag = null;
}
function finishDrag(event) {
  if (!drag || event.pointerId !== drag.pointerId) return;
  const previous = drag.previous;
  const moved = drag.moved;
  selectedId = drag.id;
  detachDrag(event.currentTarget);
  if (moved) {
    remember(previous);
    queueSave();
  }
  draw();
}
function cancelDrag(event) {
  if (!drag) return;
  room = drag.previous;
  detachDrag(event.currentTarget);
  draw();
}

/** Add at viewport centre without requiring fine motor control or dragging. */
function placeAtCentre() {
  if (!armedType || !ready) return;
  const worldX = (elements.viewport.scrollLeft + elements.viewport.clientWidth / 2) / zoom;
  const worldY = (elements.viewport.scrollTop + elements.viewport.clientHeight / 2) / zoom;
  place(armedType, worldX, worldY);
}
function place(type, worldX, worldY) {
  const info = OBJECTS[type];
  if (!info) return;
  changeRoom(addObject(room, type, crypto.randomUUID(),
    worldX - info.width / 2, worldY - info.height / 2));
  selectedId = null;
  armedType = null;
  elements.addCenter.disabled = true;
  announce(info.name + " placed, already coloured. Placement does not record a completed activity.");
  draw();
}

/** Scroll position changes on zoom, but persisted object coordinates do not. */
function setZoom(next) {
  const bounded = Math.min(1.6, Math.max(0.35, Number(next)));
  const box = elements.viewport;
  const scroll = centeredZoomScroll(zoom, bounded,
    box.scrollLeft, box.scrollTop, box.clientWidth, box.clientHeight);
  zoom = bounded;
  elements.space.style.width = WORLD.width * zoom + "px";
  elements.space.style.height = WORLD.height * zoom + "px";
  elements.scene.style.transform = "scale(" + zoom + ")";
  elements.zoomValue.textContent = Math.round(zoom * 100) + "%";
  box.scrollLeft = Math.max(0, scroll.left);
  box.scrollTop = Math.max(0, scroll.top);
}

/** Switch day without racing pending writes against the new date. */
async function changeDay(date) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return;
  ready = false;
  elements.status.textContent = "Opening room…";
  try {
    await pendingSave;
    room = await loadRoom(date) || emptyRoom(date);
    selectedId = null;
    armedType = null;
    elements.addCenter.disabled = true;
    undoStack.length = 0;
    elements.status.textContent = "This room is stored on your device";
    ready = true;
    draw();
  } catch {
    elements.status.textContent = "Unable to open saved room; editing is disabled.";
    draw();
  }
}

elements.scene.addEventListener("click", event => {
  if (!armedType || !ready || event.target !== elements.scene) return;
  const point = pointerToWorld(event.clientX, event.clientY,
    elements.scene.getBoundingClientRect(), zoom);
  place(armedType, point.x, point.y);
});
elements.addCenter.addEventListener("click", placeAtCentre);
elements.undo.addEventListener("click", () => {
  if (!ready || !undoStack.length) return;
  room = undoStack.pop();
  selectedId = null;
  draw();
  queueSave();
});
elements.bringFront.addEventListener("click", () => changeRoom(bringToFront(room, selectedId)));
elements.remove.addEventListener("click", () => {
  changeRoom(removeObject(room, selectedId));
  selectedId = null;
  draw();
});
for (const button of document.querySelectorAll("[data-nudge]")) {
  button.addEventListener("click", () => {
    const item = room.objects.find(o => o.id === selectedId);
    if (!item) return;
    const offsets = {
      left: [-20, 0], right: [20, 0], up: [0, -20], down: [0, 20]
    }[button.dataset.nudge];
    if (!offsets) return;
    changeRoom(moveObject(room, item.id, item.x + offsets[0], item.y + offsets[1]));
  });
}
byId("zoom-in").addEventListener("click", () => setZoom(zoom + 0.15));
byId("zoom-out").addEventListener("click", () => setZoom(zoom - 0.15));
byId("zoom-reset").addEventListener("click", () => setZoom(0.7));
elements.day.addEventListener("change", event => changeDay(event.target.value));
elements.deleteDay.addEventListener("click", async () => {
  if (!ready || !window.confirm("Delete this day's room from this device?")) return;
  try {
    await pendingSave;
    await deleteRoom(room.date);
    room = emptyRoom(room.date);
    undoStack.length = 0;
    selectedId = null;
    elements.status.textContent = "This day's room was deleted from this device";
    draw();
  } catch {
    elements.status.textContent = "Deletion failed. Please try again.";
  }
});
elements.deleteAll.addEventListener("click", async () => {
  if (!ready || !window.confirm("Permanently delete ALL saved prototype rooms on this device?")) return;
  try {
    await pendingSave;
    await deleteAllRooms();
    room = emptyRoom(room.date);
    undoStack.length = 0;
    selectedId = null;
    elements.status.textContent = "All prototype room data was deleted from this device";
    draw();
  } catch {
    elements.status.textContent = "Deletion failed. Please try again.";
  }
});

renderDrawers();
elements.day.value = room.date;
setZoom(zoom);
draw();
changeDay(room.date);

/** Registration is optional; running on HTTP outside localhost may disable it. */
if ("serviceWorker" in navigator && (location.protocol === "https:" ||
    ["localhost", "127.0.0.1"].includes(location.hostname))) {
  navigator.serviceWorker.register("./sw.js").catch(() => {
    // App remains useful online; avoid leaking private user context to logs.
  });
}
