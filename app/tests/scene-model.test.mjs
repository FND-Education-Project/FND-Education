/**
 * Deterministic geometry tests; no browser, external API or third-party
 * dependency required. These confirm saved data remains device-independent.
 */
import test from "node:test";
import assert from "node:assert/strict";
import {
  WORLD, MIN_VISIBLE, OBJECTS, emptyRoom, clampPosition, addObject,
  moveObject, removeObject, bringToFront, validRoom,
  centeredZoomScroll, pointerToWorld
} from "../src/scene-model.mjs";

test("empty room has a date, scene, and no assumed participation", () => {
  const room = emptyRoom("2026-10-23");
  assert.deepEqual(room, { date: "2026-10-23", sceneId: "sample", objects: [] });
  assert.ok(validRoom(room));
  assert.throws(() => emptyRoom("today"));
});

test("adding places a pre-defined object, not a completed activity", () => {
  const room = addObject(emptyRoom("2026-10-23"), "book", "id-1", 100, 210);
  assert.equal(room.objects[0].type, "book");
  assert.equal(room.objects[0].z, 1);
  assert.equal(Object.hasOwn(room.objects[0], "completed"), false);
  assert.ok(validRoom(room));
});

test("objects can intentionally clip, but retain a minimum visible handle", () => {
  const room = emptyRoom("2026-10-23");
  const { width, height } = OBJECTS.vacuum;
  const edge = clampPosition("vacuum", -999, 9999);
  assert.equal(edge.x, MIN_VISIBLE - width);
  assert.equal(edge.y, WORLD.height - MIN_VISIBLE);
  assert.ok(validRoom(addObject(room, "vacuum", "v", -999, 9999)));
  assert.equal(clampPosition("vacuum", 99999, -999).x, WORLD.width - MIN_VISIBLE);
});

test("moving and removing preserve object identity and scene state", () => {
  const initial = addObject(emptyRoom("2026-10-23"), "headphones", "a", 100, 100);
  const moved = moveObject(initial, "a", 333, 444);
  assert.equal(moved.objects[0].id, "a");
  assert.equal(moved.objects[0].x, 333);
  assert.equal(initial.objects[0].x, 100);
  assert.deepEqual(removeObject(moved, "a").objects, []);
});

test("stacking is deliberate: selected rear item can move in front", () => {
  let room = addObject(emptyRoom("2026-10-23"), "book", "rear", 90, 90);
  room = addObject(room, "vacuum", "front", 90, 90);
  assert.ok(room.objects[1].z > room.objects[0].z);
  room = bringToFront(room, "rear");
  assert.ok(room.objects[0].z > room.objects[1].z);
  assert.ok(validRoom(room));
});

test("a viewport-center zoom keeps the same world point centered", () => {
  const old = { left: 340, top: 60, width: 360, height: 280, zoom: 0.65 };
  const nextZoom = 1.1;
  const next = centeredZoomScroll(old.zoom, nextZoom, old.left, old.top, old.width, old.height);
  const oldCenter = (old.left + old.width / 2) / old.zoom;
  const newCenter = (next.left + old.width / 2) / nextZoom;
  assert.ok(Math.abs(oldCenter - newCenter) < 1e-8);
  const oldY = (old.top + old.height / 2) / old.zoom;
  const newY = (next.top + old.height / 2) / nextZoom;
  assert.ok(Math.abs(oldY - newY) < 1e-8);
});

test("pointer screen coordinates translate into unscaled world coordinates", () => {
  assert.deepEqual(pointerToWorld(410, 290, { left: 110, top: 90 }, 0.5), { x: 600, y: 400 });
});

test("saved records reject invalid sprites and geometry", () => {
  const room = addObject(emptyRoom("2026-10-23"), "book", "id", 0, 0);
  assert.ok(validRoom(room));
  assert.equal(validRoom({ ...room, objects: [{ ...room.objects[0], type: "unknown" }] }), false);
  assert.equal(validRoom({ ...room, objects: [room.objects[0], room.objects[0]] }), false);
  assert.equal(validRoom({ ...room, objects: [{ ...room.objects[0], x: Infinity }] }), false);
  assert.equal(validRoom({ ...room, objects: [{ ...room.objects[0], x: 1e6 }] }), false);
});

test("unsupported additions cannot silently enter the room", () => {
  assert.throws(() => addObject(emptyRoom("2026-10-23"), "medical-score", "x", 0, 0));
  assert.throws(() => clampPosition("book", NaN, 0));
});
