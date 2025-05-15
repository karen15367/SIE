document.addEventListener("DOMContentLoaded", function () {
    var openPopupButton = document.getElementById("btnAvisos");
    var popup = document.getElementById("dvAvisos");
    var closePopupButton = document.getElementById("closePopup");
    if (openPopupButton) {
        openPopupButton.addEventListener("click", function () {
            if (popup) {
                popup.style.display = "block";
            }
        });
    }
    if (openPopupButton) {
        openPopupButton.addEventListener("click", function () {
            if (popup) {
                popup.style.display = "block";
            }
        });
    }
    if (closePopupButton) {
        closePopupButton.addEventListener("click", function () {
            if (popup) {
                popup.style.display = "none";
            }
        });
    }
    if (popup) {
        window.addEventListener("click", function (event) {
            if (event.target === popup) {
                popup.style.display = "none";
            }
        });
    }
});
