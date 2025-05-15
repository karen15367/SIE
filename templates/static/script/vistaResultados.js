// 1. Obtenemos referencias
const selectCarrera = document.getElementById("carrera");
const inputSearch = document.getElementById("q");

// 2. Escuchamos cambios en el <select>
selectCarrera.addEventListener("change", () => {
    // Si el valor es distinto de la opción vacía, deshabilitamos el input
    if (selectCarrera.value !== "") {
        inputSearch.disabled = true; // :contentReference[oaicite:0]{index=0}
        inputSearch.value = ""; // opcional: limpiar texto previo
    } else {
        // Si se vuelve a la opción por defecto, lo habilitamos de nuevo
        inputSearch.disabled = false; // :contentReference[oaicite:1]{index=1}
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll("#tabla-egresados td");

    cells.forEach((td) => {
        let style = window.getComputedStyle(td);
        let fontSize = parseFloat(style.fontSize);

        // Mientras desborde y no se reduzca demasiado
        while (td.scrollWidth > td.clientWidth && fontSize > 8) {
            fontSize -= 1; // reducir 1px
            td.style.fontSize = fontSize + "px";
        }
    });
});
