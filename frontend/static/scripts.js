document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.form-control').forEach(function(textArea) {
        textArea.style.height = textArea.scrollHeight + 'px';
        textArea.style.overflowY = 'hidden';
        textArea.addEventListener('input', function() {
            textArea.style.height = 'auto';
            textArea.style.height = textArea.scrollHeight + 'px';
        });
    });
});