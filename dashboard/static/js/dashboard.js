/* PPML/FHE Dashboard — Frontend JavaScript */

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss flash messages after 5 seconds
    document.querySelectorAll('[class*="bg-green-100"], [class*="bg-red-100"]').forEach(function (el) {
        if (el.closest('main') || el.closest('.px-4.pt-4')) {
            setTimeout(function () {
                el.style.transition = 'opacity 0.3s';
                el.style.opacity = '0';
                setTimeout(function () { el.remove(); }, 300);
            }, 5000);
        }
    });

    // Keyboard shortcut: Ctrl+K to focus search
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            var searchInput = document.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
    });

    // Confirm before navigating away from unsaved forms
    var forms = document.querySelectorAll('form textarea');
    forms.forEach(function (textarea) {
        var original = textarea.value;
        textarea.addEventListener('input', function () {
            textarea.dataset.dirty = textarea.value !== original ? '1' : '';
        });
    });

    window.addEventListener('beforeunload', function (e) {
        var dirty = document.querySelector('textarea[data-dirty="1"]');
        if (dirty) {
            e.preventDefault();
            e.returnValue = '';
        }
    });

    // Mark form as clean on submit
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function () {
            form.querySelectorAll('textarea').forEach(function (ta) {
                ta.dataset.dirty = '';
            });
        });
    });
});
