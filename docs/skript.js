document.addEventListener("DOMContentLoaded", () => {
    // Клік по блоках з URL (Monobank, Patreon)
    document.querySelectorAll('.donate').forEach(el => {
      const url = el.dataset.url;
      if (url) {
        el.addEventListener('click', e => {
          window.open(url, '_blank');
        });
      }
    });

  function showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.className = "toast show";
    setTimeout(() => {
      toast.className = toast.className.replace("show", "");
    }, 2000);
  }

  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', e => {
      const value = card.getAttribute('data-value');
      navigator.clipboard.writeText(value).then(() => {
        showToast("Copied: " + value + " ✅");
      });
    });
  });


});