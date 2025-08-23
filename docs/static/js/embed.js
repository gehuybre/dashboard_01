// Auto-height iframe system and embed snippet UX
(function () {
  function setH(el, h) { el.style.height = Math.max(240, Math.ceil(h)) + "px"; }

  // Listen for height messages from the *embed page*
  window.addEventListener("message", function (e) {
    var d = e.data || {};
    if (d.type !== "plotly-embed-size") return;
    // If you include slug targeting, keep it; else set all marked iframes.
    document.querySelectorAll('iframe[data-embed-autoheight]').forEach(function (ifr) {
      if (!d.slug || ifr.getAttribute('data-embed-slug') === d.slug) setH(ifr, d.height);
    });
  });

  // Optional: ping children so they respond immediately on load
  function ping() {
    document.querySelectorAll('iframe[data-embed-autoheight]').forEach(function (ifr) {
      try { ifr.contentWindow && ifr.contentWindow.postMessage({ type: "plotly-embed-ping" }, "*"); } catch (e) {}
    });
  }
  document.addEventListener("DOMContentLoaded", ping);
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
