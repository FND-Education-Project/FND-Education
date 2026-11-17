/**
 * Minimal local repository for the Phase 0 Activity Room.
 *
 * IndexedDB holds scene coordinates only. No symptom, journal, or course
 * account information is present in this prototype. All operations are
 * transactional and reject on failure rather than claiming data was saved.
 */
import { validRoom } from "./scene-model.mjs";

const DATABASE = "my-fnd-journey-phase0";
const VERSION = 1;
const STORE = "rooms";

/** Open the versioned local database; upgrades must never wipe existing rooms. */
function openDatabase() {
  return new Promise((resolve, reject) => {
    if (!globalThis.indexedDB) {
      reject(new Error("Local storage is unavailable in this browser"));
      return;
    }
    const request = indexedDB.open(DATABASE, VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(STORE)) {
        db.createObjectStore(STORE, { keyPath: "date" });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(new Error("Could not open device storage"));
    request.onblocked = () => reject(new Error("Another app tab is blocking the database update"));
  });
}

/** Finish a transaction only when the browser confirms the entire commit. */
async function transact(mode, action) {
  const db = await openDatabase();
  try {
    return await new Promise((resolve, reject) => {
      const transaction = db.transaction(STORE, mode);
      let result;
      transaction.oncomplete = () => resolve(result);
      transaction.onerror = () => reject(new Error("Device storage transaction failed"));
      transaction.onabort = () => reject(new Error("Device storage operation was cancelled"));
      try {
        const request = action(transaction.objectStore(STORE));
        if (request) {
          request.onsuccess = () => { result = request.result; };
          request.onerror = () => {
            // The transaction's abort/error handler reports the failure.
          };
        }
      } catch (error) {
        transaction.abort();
      }
    });
  } finally {
    db.close();
  }
}

/** Read a single day's room; invalid data is never shown as a valid layout. */
export async function loadRoom(date) {
  const value = await transact("readonly", store => store.get(date));
  if (value === undefined) return null;
  if (!validRoom(value)) throw new Error("Saved room is invalid or incompatible");
  return value;
}

/** Store validated coordinates; no images or rendered screenshots are saved. */
export async function saveRoom(room) {
  if (!validRoom(room)) throw new Error("Room could not be saved: invalid structure");
  await transact("readwrite", store => store.put(room));
}

/** Delete one day without affecting the layouts for other dates. */
export async function deleteRoom(date) {
  await transact("readwrite", store => store.delete(date));
}

/** Delete all prototype rooms on this browser/device only. */
export async function deleteAllRooms() {
  await transact("readwrite", store => store.clear());
}
