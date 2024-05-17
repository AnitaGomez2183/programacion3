document.addEventListener("DOMContentLoaded", (event) => {
    document
        .getElementById("add-option-btn")
        .addEventListener("click", addOption);
    document
        .getElementById("open-modal-btn")
        .addEventListener("click", openModal);
    document
        .getElementById("close-modal-btn")
        .addEventListener("click", closeModal);
    document
        .querySelector(".modal-background")
        .addEventListener("click", closeModal);
});

function addOption() {
    const container = document.getElementById("options-container");
    const inputDiv = document.createElement("div");
    inputDiv.className = "control option-input mb-1";
    inputDiv.innerHTML =
        '<input class="input" type="text" name="options" placeholder="Opción" required>';
    container.appendChild(inputDiv);
}

function openModal() {
    document.getElementById("modal").classList.add("is-active");
}

function closeModal() {
    document.getElementById("modal").classList.remove("is-active");
}
