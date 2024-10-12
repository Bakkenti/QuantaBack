document.addEventListener('DOMContentLoaded', function() {
    const inlines = document.querySelectorAll('.inline-related');

    inlines.forEach(function(inline) {
        const nameField = inline.querySelector('.field-name input');  // Lesson Name field
        const toggleIcon = document.createElement('span');

        // Create the dropdown toggle icon (a simple arrow)
        toggleIcon.textContent = '▼';
        toggleIcon.style.cursor = 'pointer';
        toggleIcon.style.marginLeft = '10px';

        // Initially hide content and short_description
        const contentField = inline.querySelector('.field-content');
        const shortDescriptionField = inline.querySelector('.field-short_description');
        contentField.style.display = 'none';
        shortDescriptionField.style.display = 'none';

        // Append the toggle icon next to the name field
        nameField.parentNode.appendChild(toggleIcon);

        // Add the toggle functionality
        toggleIcon.addEventListener('click', function() {
            if (contentField.style.display === 'none') {
                contentField.style.display = 'block';
                shortDescriptionField.style.display = 'block';
                toggleIcon.textContent = '▲';  // Change to collapse icon
            } else {
                contentField.style.display = 'none';
                shortDescriptionField.style.display = 'none';
                toggleIcon.textContent = '▼';  // Change to expand icon
            }
        });
    });
});
