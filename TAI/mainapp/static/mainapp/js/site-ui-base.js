// site-ui-base.js

document.addEventListener('DOMContentLoaded', () => {
    // === Hamburger Menu Toggle ===
    const hamburgerBtn = document.getElementById('hamburgerBtn'); // Button that toggles the menu
    const navLinks = document.getElementById('navLinks'); // Navigation links container

    hamburgerBtn.addEventListener('click', () => {
        // Toggle 'active' class on button and nav links to open/close menu
        hamburgerBtn.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // === User Dropdown Toggle ===
    const userPic = document.querySelector('.user-pic'); // User profile picture (button)
    const userDropdown = document.getElementById('userDropdown'); // Dropdown menu for user options

    if (userPic) {
        userPic.addEventListener('click', () => {
            // Toggle 'active' class to show/hide user dropdown
            userDropdown.classList.toggle('active');
        });
    }

    // === Theme Toggle ===
    const themeToggleBtn = document.getElementById('themeToggleBtn'); // Button to toggle theme

    themeToggleBtn.addEventListener('click', () => {
        // Toggle 'dark-theme' class on the body
        document.body.classList.toggle('dark-theme');

        // Save current theme preference to localStorage
        const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
        localStorage.setItem('theme', currentTheme);
    });

    // === Load Theme from Local Storage ===
    if (localStorage.getItem('theme') === 'dark') {
        // Apply dark theme if saved preference is 'dark'
        document.body.classList.add('dark-theme');
    }
});
