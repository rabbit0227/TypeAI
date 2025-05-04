document.addEventListener('DOMContentLoaded', () => {
    // Hamburger Menu Toggle
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navLinks = document.getElementById('navLinks');

    hamburgerBtn.addEventListener('click', () => {
        hamburgerBtn.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // User Dropdown Toggle
    const userPic = document.querySelector('.user-pic');
    const userDropdown = document.getElementById('userDropdown');

    if (userPic) {
        userPic.addEventListener('click', () => {
            userDropdown.classList.toggle('active');
        });
    }

    // Theme Toggle
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
    });

    // Load Theme from Local Storage
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-theme');
    }
});