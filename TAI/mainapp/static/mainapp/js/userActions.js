// User action functions
async function shareText() {
    try {
        await navigator.clipboard.writeText(elements.editor.value);
        addLogEntry('Text shared');
        alert('Text copied to clipboard for sharing!');
    } catch (err) {
        console.error('Share failed:', err);
    }
}

function saveText() {
    localStorage.setItem('savedText', elements.editor.value);
    addLogEntry('Text saved');
    alert('Text saved!');
}

function addCollaborator() {
    addLogEntry('Collaborator added');
    alert('Add collaborator feature not yet implemented.');
}

function openSettings() {
    addLogEntry('Settings opened');
    alert('Settings feature not yet implemented.');
}

function logout() {
    addLogEntry('User logged out');
    alert('Logout feature not yet implemented.');
}