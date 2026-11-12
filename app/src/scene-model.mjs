/**
 * Pure Activity Room geometry and data rules.
 *
 * No DOM, persistence, network requests, or medical interpretation belongs here.
 * All coordinates are in a fixed scene "world" so that changing the device
 * size or zoom never changes a saved object's position.
 */
export const WORLD = Object.freeze({ width: 1280, height: 720 });
export const MIN_VISIBLE = 48;

/** Deliberately small temporary object catalogue for the Phase 0 spike. */
export const OBJECTS = Object.freeze({
  vacuum: Object.freeze({ name: "Vacuum", drawer: "Chores", symbol: "🧹", width: 112, height: 96 }),
  book: Object.freeze({ name: "Book", drawer: "Rest & relax", symbol: "📖", width: 112, height: 96 }),
  headphones: Object.freeze({ name: "Headphones", drawer: "Positive activities", symbol: "🎧", width: 112, height: 96 })
});

/** Create a dated room without recording any health information. */
export function emptyRoom(date) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error("Invalid local date");
  return { date, sceneId: "sample", objects: [] };
}

/** Keep some visible grabbing area even when a sprite is intentionally clipped. */
export function clampPosition(type, x, y, scale = 1) {
  const definition = OBJECTS[type];
  if (!definition || !Number.isFinite(x) || !Number.isFinite(y) ||
      !Number.isFinite(scale) || scale <= 0 || scale > 4) {
    throw new Error("Invalid sprite geometry");
  }
  const w = definition.width * scale;
  const h = definition.height * scale;
  return {
    x: Math.round(Math.max(MIN_VISIBLE - w, Math.min(WORLD.width - MIN_VISIBLE, x))),
    y: Math.round(Math.max(MIN_VISIBLE - h, Math.min(WORLD.height - MIN_VISIBLE, y)))
  };
}

/** A placed object represents a visual choice, not completed activity. */
export function addObject(room, type, id, x, y) {
  if (!OBJECTS[type] || typeof id !== "string" || !id || room.objects.some(o => o.id === id)) {
    throw new Error("Invalid new object");
  }
  const point = clampPosition(type, x, y);
  const top = Math.max(0, ...room.objects.map(o => o.z));
  return {
    ...room,
    objects: [...room.objects, { id, type, x: point.x, y: point.y, z: top + 1, scale: 1 }]
  };
}

/** Move an item without altering its identity, colour, or optional future notes. */
export function moveObject(room, id, x, y) {
  const old = room.objects.find(o => o.id === id);
  if (!old) return room;
  const point = clampPosition(old.type, x, y, old.scale);
  return { ...room, objects: room.objects.map(o => o.id === id ? { ...o, ...point } : o) };
}

/** Explicit reordering, not click-through of sprites hidden behind other sprites. */
export function bringToFront(room, id) {
  if (!room.objects.some(o => o.id === id)) return room;
  const top = Math.max(0, ...room.objects.map(o => o.z)) + 1;
  return { ...room, objects: room.objects.map(o => o.id === id ? { ...o, z: top } : o) };
}

export function removeObject(room, id) {
  return { ...room, objects: room.objects.filter(o => o.id !== id) };
}

/**
 * Preserve the world point under the VIEWPORT CENTRE on zoom.
 * Browser scrolling will naturally clamp if the content becomes smaller.
 */
export function centeredZoomScroll(oldZoom, nextZoom, scrollLeft, scrollTop, viewportWidth, viewportHeight) {
  if (![oldZoom, nextZoom, scrollLeft, scrollTop, viewportWidth, viewportHeight]
      .every(Number.isFinite) || oldZoom <= 0 || nextZoom <= 0) {
    throw new Error("Invalid viewport state");
  }
  return {
    left: (scrollLeft + viewportWidth / 2) * nextZoom / oldZoom - viewportWidth / 2,
    top: (scrollTop + viewportHeight / 2) * nextZoom / oldZoom - viewportHeight / 2
  };
}

/** Convert a pointer position on the transformed scene back to world units. */
export function pointerToWorld(clientX, clientY, rect, zoom) {
  if (!Number.isFinite(zoom) || zoom <= 0) throw new Error("Invalid zoom");
  return { x: (clientX - rect.left) / zoom, y: (clientY - rect.top) / zoom };
}

/** Reject malformed or stale imported records rather than executing or trusting them. */
export function validRoom(room) {
  if (!room || typeof room !== "object" || !/^\d{4}-\d{2}-\d{2}$/.test(room.date) ||
      room.sceneId !== "sample" || !Array.isArray(room.objects) ||
      room.objects.length > 300) return false;
  const ids = new Set();
  for (const object of room.objects) {
    if (!object || typeof object.id !== "string" || object.id.length > 100 ||
        ids.has(object.id) || !OBJECTS[object.type] ||
        ![object.x, object.y, object.z, object.scale].every(Number.isFinite) ||
        !Number.isInteger(object.z) || object.z < 0 || object.scale <= 0 || object.scale > 4) {
      return false;
    }
    const clamped = clampPosition(object.type, object.x, object.y, object.scale);
    if (object.x !== clamped.x || object.y !== clamped.y) return false;
    ids.add(object.id);
  }
  return true;
}
