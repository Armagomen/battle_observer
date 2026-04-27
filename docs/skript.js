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

    // Клік по блоках з данними для копіювання в буфер
    function showToast(message) {
        const toast = document.getElementById("toast");
        toast.textContent = message;
        toast.className = "toast show";
        setTimeout(() => {
            toast.className = toast.className.replace("show", "");
        }, 2000);
    }

    document.querySelectorAll('.copy_value').forEach(copy_value => {
        copy_value.addEventListener('click', e => {
            const value = copy_value.getAttribute('data-value');
            navigator.clipboard.writeText(value).then(() => {
                showToast("Copied: " + value + " ✅");
            });
        });
    });

    async function loadMonoProgress() {
        try {
            const longJarId = "2zQL6sqnKgTYi7e69271YYWKTXTfMK8g";
            const response = await fetch(`https://api.monobank.ua/bank/jar/${longJarId}`);
            const monoApi = await response.json();

            const amount = monoApi.amount / 100;
            const goal = monoApi.goal / 100;
            const percent = (amount / goal) * 100;

            document.querySelector(".progress-bar").style.width = percent + "%";
            document.getElementById("progress-text").innerText =
                `Зібрано ${amount.toFixed(2)} ₴ із ${goal} ₴`;

        } catch (e) {
            document.getElementById("progress-text").innerText = "Не вдалося завантажити дані";
            console.error(e);
        }
    }

    loadMonoProgress();


});