document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('banks-link').addEventListener('click', function (event) {
        event.preventDefault(); // Prevents navigation to the link
        var bar = document.getElementById('bar');

        // Toggle the visibility of the bar when the BANKS link is clicked
        if (bar.classList.contains('hidden')) {
            bar.classList.remove('hidden');
            bar.classList.add('visible');
        } else {
            bar.classList.remove('visible');
            bar.classList.add('hidden');
        }
    });
});