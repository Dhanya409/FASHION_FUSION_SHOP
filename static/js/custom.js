// js for auto-generating slug
document.addEventListener("DOMContentLoaded", function () {
    // Get the name and slug input elements
    var nameInput = document.getElementById("name");
    var slugInput = document.getElementById("slug");

    // Function to generate the slug from the name
    function generateSlug() {
        var nameValue = nameInput.value.trim();
        var slugValue = nameValue.toLowerCase().replace(/ /g, "-");
        slugInput.value = slugValue;
    }

    // Add an input event listener to the name input
    nameInput.addEventListener("input", generateSlug);
});

// js for deleting product
