// Event handling and initialization
const handleInput = debounce(() => {
    resetState();
    updateTokenCount();
}, 300);

// Event listeners
elements.editor.addEventListener('input', handleInput);
// elements.themeToggleBtn.addEventListener('click', () => {
//     document.body.classList.toggle('dark-theme');
//     const isDark = document.body.classList.contains('dark-theme');
//     localStorage.setItem('theme', isDark ? 'dark' : 'light');
//     elements.themeToggleBtn.textContent = isDark ? 'Light Theme' : 'Dark Theme';
// });

// elements.userPic.addEventListener('click', () => {
//     elements.userDropdown.classList.toggle('active');
// });

// elements.hamburgerBtn.addEventListener('click', () => {
//     elements.navLinks.classList.toggle('active');
//     elements.hamburgerBtn.classList.toggle('active');
// });

elements.updateFromDbBtn.addEventListener('click', updateFromFile);
elements.saveToDbBtn.addEventListener('click', storeToDB);

// Close dropdown when clicking outside
// document.addEventListener('click', (e) => {
//     if (!elements.userMenu.contains(e.target)) {
//         elements.userDropdown.classList.remove('active');
//     }
//     if (!elements.navLinks.contains(e.target) && !elements.hamburgerBtn.contains(e.target)) {
//         elements.navLinks.classList.remove('active');
//         elements.hamburgerBtn.classList.remove('active');
//     }
// });

// Initialize theme and token count
// document.addEventListener('DOMContentLoaded', () => {
//     if (localStorage.getItem('theme') === 'dark') {
//         document.body.classList.add('dark-theme');
//         elements.themeToggleBtn.textContent = 'Light Theme';
//     }
//     updateTokenCount();
// });