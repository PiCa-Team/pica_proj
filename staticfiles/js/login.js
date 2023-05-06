document.addEventListener("DOMContentLoaded", function() {
    const inputFields = document.querySelectorAll(".input-field input");

    inputFields.forEach(input => {
        input.addEventListener("input", () => {
            if (input.value !== "") {
                input.classList.add("not-empty");
            } else {
                input.classList.remove("not-empty");
            }
        });
    });
});
