// Sidebar toggle
function toggleSidebar() {
    document.body.classList.toggle('sidebar-collapsed');
    // Save preference
    localStorage.setItem('sidebarCollapsed', document.body.classList.contains('sidebar-collapsed'));
}

// Load sidebar state
if (localStorage.getItem('sidebarCollapsed') === 'true') {
    document.body.classList.add('sidebar-collapsed');
}

// Global search handler
function handleSearch(event) {
    if (event.key === 'Enter') {
        const query = event.target.value.trim();
        if (query) {
            // Redirect to students page with search query
            window.location.href = `/students?q=${encodeURIComponent(query)}`;
        }
    }
}

// Toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            if (flash && flash.parentElement) {
                flash.style.opacity = '0';
                flash.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    if (flash && flash.parentElement) flash.remove();
                }, 300);
            }
        }, 5000);
    });
});

// Confirm delete functions (global)
window.confirmDelete = function(message, url) {
    if (confirm(message)) {
        fetch(url, { method: 'POST' })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    window.location.reload();
                }
            })
            .catch(err => {
                showToast('Error deleting item', 'error');
            });
    }
    return false;
};
