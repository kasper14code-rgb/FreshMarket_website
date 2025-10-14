document.addEventListener('DOMContentLoaded', function() {
    // Active navigation
    const navLinks = document.querySelectorAll('.sidebar .nav-links li');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 5000);
    });

    console.log('FreshMart Dashboard loaded successfully');
});