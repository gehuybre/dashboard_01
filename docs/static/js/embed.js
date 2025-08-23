// Auto-height iframe system and embed snippet UX
(function () {
  function setH(el, h) { el.style.height = Math.max(300, Math.ceil(h)) + "px"; }
  function onMessage(e) {
    var d = e.data || {};
    if (d.type !== "plotly-embed-size") return;
    document.querySelectorAll('iframe[data-embed-autoheight]').forEach(function (ifr) {
      if (!d.slug || ifr.getAttribute('data-embed-slug') === d.slug) setH(ifr, d.height);
    });
  }
  function ping() {
    document.querySelectorAll('iframe[data-embed-autoheight]').forEach(function (ifr) {
      try { if (ifr.contentWindow) ifr.contentWindow.postMessage({ type: "plotly-embed-ping" }, "*"); } catch (e) {}
    });
  }

  window.addEventListener("message", onMessage);

  // Initial load
  document.addEventListener("DOMContentLoaded", ping);

  // Re-run after every SPA navigation in Material
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(function () { ping(); });
  }
})();

// Enhancements for embed snippet UX (copy on click if desired)
document.addEventListener('click', (e) => {
  const pre = e.target.closest('pre');
  if (pre && pre.innerText.includes('<iframe')) {
    navigator.clipboard?.writeText(pre.innerText.trim()).then(()=>{
      const old = pre.getAttribute('data-copied');
      pre.setAttribute('data-copied','copied');
      setTimeout(()=> pre.removeAttribute('data-copied'), 1200);
    }).catch(()=>{});
  }
});
