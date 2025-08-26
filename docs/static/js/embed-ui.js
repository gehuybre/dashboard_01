(function () {
  function absUrl(path) {
    var siteUrl = (window?.location?.origin + window?.location?.pathname.replace(/\/[^/]*$/, "")) || "";
    // We pass absolute URLs from Python; this is just a safeguard.
    if (/^https?:\/\//i.test(path)) return path;
    return (window?.__SITE_URL__ || "").replace(/\/$/, "") + "/" + String(path || "").replace(/^\//, "");
  }

  function buildCode(src, w, h, title, noborder) {
    var style = noborder ? ' style="border:0;"' : "";
    return `<iframe src="${src}" width="${w}" height="${h}" loading="lazy" title="${title}"${style}></iframe>`;
  }

  function initOne(box) {
    var slug   = box.getAttribute("data-embed-slug") || "";
    var src    = box.getAttribute("data-embed-src");
    var wEl    = box.querySelector(".embed-width");
    var hEl    = box.querySelector(".embed-height");
    var bEl    = box.querySelector(".embed-border");
    var ta     = box.querySelector(".embed-code");
    var copyBt = box.querySelector(".embed-copy");

    function update() {
      var code = buildCode(src, wEl.value || 800, hEl.value || 480, slug, bEl.checked);
      ta.value = code;
    }
    update();

    box.addEventListener("input", function (e) {
      if (e.target.matches(".embed-width, .embed-height, .embed-border")) update();
    });

    copyBt.addEventListener("click", async function () {
      try {
        await navigator.clipboard.writeText(ta.value);
        copyBt.textContent = "Copied!";
        setTimeout(() => (copyBt.textContent = "Copy"), 1200);
      } catch (e) {
        ta.select(); document.execCommand("copy");
      }
    });
  }

  function initAll() {
    document.querySelectorAll(".embed-ui").forEach(initOne);
  }

  document.addEventListener("DOMContentLoaded", initAll);
  if (window.document$ && typeof window.document$.subscribe === "function") {
    // MkDocs Material instant navigation
    window.document$.subscribe(function () { setTimeout(initAll, 50); });
  }
})();
