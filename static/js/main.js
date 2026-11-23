document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile navigation toggle
    const navToggle = document.getElementById("navToggle");
    const mainNav = document.getElementById("mainNav");

    if (navToggle && mainNav) {
        navToggle.addEventListener("click", () => {
            mainNav.classList.toggle("open");
        });
    }

    // 2. Dismiss alert messages
    document.querySelectorAll(".alert-close").forEach((btn) => {
        btn.addEventListener("click", () => {
            const alertBox = btn.closest(".alert");
            if (alertBox) {
                alertBox.remove();
            }
        });
    });

    // 3. Project detail gallery switcher
    const mainPreviewImg = document.getElementById("activeProjectImage");
    const captionEl = document.getElementById("activeImageCaption");
    const thumbs = document.querySelectorAll(".thumb-item");

    if (mainPreviewImg && thumbs.length > 0) {
        thumbs.forEach((thumb) => {
            thumb.addEventListener("click", () => {
                const newSrc = thumb.getAttribute("data-src");
                const newCaption = thumb.getAttribute("data-caption");

                if (newSrc) {
                    mainPreviewImg.src = newSrc;
                }
                if (captionEl && newCaption) {
                    captionEl.textContent = newCaption;
                }

                thumbs.forEach((item) => item.classList.remove("active"));
                thumb.classList.add("active");
            });
        });
    }
});