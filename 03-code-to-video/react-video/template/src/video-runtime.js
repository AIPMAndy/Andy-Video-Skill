if (typeof window !== "undefined" && typeof window.__VIDEO_READY__ === "undefined") {
  window.__VIDEO_READY__ = false;
}

export function setVideoDuration(ms) {
  if (typeof window !== "undefined") {
    window.__VIDEO_DURATION_MS__ = ms;
  }
}

export function markVideoReady() {
  if (typeof window !== "undefined") {
    window.__VIDEO_READY__ = true;
  }
}

export function markVideoNotReady() {
  if (typeof window !== "undefined") {
    window.__VIDEO_READY__ = false;
  }
}
