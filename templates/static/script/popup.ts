document.addEventListener("DOMContentLoaded", () => {
    const openPopupButton = document.getElementById("btnAvisos") as HTMLButtonElement | null;
    const popup = document.getElementById("dvAvisos") as HTMLDivElement | null;
    const closePopupButton = document.getElementById("closePopup") as HTMLSpanElement | null;

    if (popup) {
        popup.style.display = "block";
    }

    if (openPopupButton) {
        openPopupButton.addEventListener("click", () => {
            if (popup) {
                popup.style.display = "block";
            }
        });
    }

    if (closePopupButton) {
        closePopupButton.addEventListener("click", () => {
            if (popup) {
                popup.style.display = "none";
            }
        });
    }

    if (popup) {
        window.addEventListener("click", (event) => {
            if (event.target === popup) {
                popup.style.display = "none";
            }
        });
    }
});