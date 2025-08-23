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
