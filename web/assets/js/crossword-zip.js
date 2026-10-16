/* Small standards-compliant ZIP writer (stored files, no external service). */
(function (root) {
  "use strict";
  const encoder = new TextEncoder();
  function crc32(bytes) {
    let crc = -1;
    for (const byte of bytes) {
      crc ^= byte;
      for (let i = 0; i < 8; i++) {
        crc = (crc >>> 1) ^ (crc & 1 ? 0xEDB88320 : 0);
      }
    }
    return (crc ^ -1) >>> 0;
  }
  function zip(files) {
    if (!Array.isArray(files) || !files.length || files.length > 10) {
      throw new Error("ZIP expects 1 to 10 files.");
    }
    const local = [], central = [];
    let offset = 0, centralSize = 0;
    for (const entry of files) {
      if (!/^[a-z0-9._-]{1,110}$/i.test(entry.name) || !(entry.bytes instanceof Uint8Array)) {
        throw new Error("Invalid ZIP filename or contents.");
      }
      const name = encoder.encode(entry.name), bytes = entry.bytes;
      if (bytes.length > 40 * 1024 * 1024) throw new Error("ZIP file is too large.");
      const crc = crc32(bytes);
      const head = new Uint8Array(30 + name.length), h = new DataView(head.buffer);
      h.setUint32(0, 0x04034b50, true);
      h.setUint16(4, 20, true);     // version needed
      h.setUint16(8, 0, true);      // no compression
      h.setUint32(14, crc, true);
      h.setUint32(18, bytes.length, true);
      h.setUint32(22, bytes.length, true);
      h.setUint16(26, name.length, true);
      head.set(name, 30);
      local.push(head, bytes);
      const directory = new Uint8Array(46 + name.length), d = new DataView(directory.buffer);
      d.setUint32(0, 0x02014b50, true);
      d.setUint16(4, 20, true); d.setUint16(6, 20, true);
      d.setUint32(16, crc, true);
      d.setUint32(20, bytes.length, true);
      d.setUint32(24, bytes.length, true);
      d.setUint16(28, name.length, true);
      d.setUint32(42, offset, true);
      directory.set(name, 46);
      central.push(directory);
      centralSize += directory.length;
      offset += head.length + bytes.length;
    }
    const ending = new Uint8Array(22), e = new DataView(ending.buffer);
    e.setUint32(0, 0x06054b50, true);
    e.setUint16(8, files.length, true);
    e.setUint16(10, files.length, true);
    e.setUint32(12, centralSize, true);
    e.setUint32(16, offset, true);
    const pieces = [...local, ...central, ending];
    const size = pieces.reduce((sum, part) => sum + part.length, 0);
    const output = new Uint8Array(size);
    let at = 0;
    for (const part of pieces) { output.set(part, at); at += part.length; }
    return output;
  }
  const api = { zip, crc32 };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.FNDCrosswordZip = api;
})(typeof window === "undefined" ? null : window);
