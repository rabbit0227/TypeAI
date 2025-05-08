// Initialize Typo dictionary
const dictionary = new Typo('en_US', false, false, {
    dictionaryPath: 'https://unpkg.com/typo-js@1.2.4/dictionaries'
});

// Cache DOM elements
const elements = {
    editor:                 document.getElementById('editor'),
    correctionsArea:        document.getElementById('correctionsArea'),
    showCorrectedBtn:       document.getElementById('showCorrectedBtn'),
    diffArea:               document.getElementById('diffArea'),
    updateBtn:              document.getElementById('updateBtn'),
    showWrongBtn:           document.getElementById('showWrongBtn'),
    confirmationButtons:    document.getElementById('confirmationButtons'),
    activityLog:            document.getElementById('activityLog'),
    themeToggleBtn:         document.getElementById('themeToggleBtn'),
    userPic:                document.querySelector('.user-pic'),
    userDropdown:           document.getElementById('userDropdown'),
    availableTokens:        document.getElementById('availableTokens'),
    usedTokens:             document.getElementById('usedTokens'),
    hamburgerBtn:           document.getElementById('hamburgerBtn'),
    navLinks:               document.getElementById('navLinks'),
    updateFromDbBtn:        document.getElementById('updateFileBtn'),
    saveToDbBtn:            document.getElementById('saveBtn'),
    lastSaved:              document.getElementById('lastSaved'),
    userMenu:               document.getElementById('userMenu'),
    
};

// State management
let state = {
    correctedText: '',
    asteriskText: '',
    wrongWords: [],
    isCorrectedVisible: false,
    isWrongWordsVisible: false,
    updateSource: 'spelling',
    selectionStart: 0,
    selectionEnd: 0,
    fullCorrectedText: ''
};

// Memoization cache for spelling checks
const spellingCache = new Map();

// Debounce utility
const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
    };
};

// Update token count
function updateTokenCount() {
    const text = elements.editor.value;
    const usedTokens = text.trim() ? text.split(/\s+/).length : 0;
    const maxTokens = 1000; // Example max tokens
    elements.usedTokens.textContent = `Used Tokens: ${usedTokens}`;
    elements.availableTokens.textContent = `Available Tokens: ${maxTokens - usedTokens}`;
}

// Check spelling for selected or full text
function checkSpelling() {
    const fullText = elements.editor.value;
    state.selectionStart = elements.editor.selectionStart;
    state.selectionEnd = elements.editor.selectionEnd;

    let textToCheck = fullText;
    let isPartial = false;
    if (state.selectionStart !== state.selectionEnd) {
        textToCheck = fullText.substring(state.selectionStart, state.selectionEnd);
        isPartial = true;
    }

    if (!textToCheck.trim()) {
        resetCorrections();
        return;
    }

    const cacheKey = `${textToCheck}_${state.selectionStart}_${state.selectionEnd}`;
    if (spellingCache.has(cacheKey)) {
        const { correctedText, asteriskText, wrongWords } = spellingCache.get(cacheKey);
        updateCorrections(correctedText, asteriskText, wrongWords, isPartial, fullText);
        return;
    }

    const words = textToCheck.split(/(\s+)/);
    let correctedWords = '';
    const wrongWords = [];
    let asteriskText = '';
    let wrongWordCount = 0;

    for (let i = 0; i < words.length; i++) {
        const word = words[i];
        const isWhitespace = /\s+/.test(word);
        const cleanWord = word.replace(/[.,!?]/g, '');

        if (!isWhitespace && cleanWord && !dictionary.check(cleanWord)) {
            wrongWordCount++;
            wrongWords.push(cleanWord);
            const suggestions = dictionary.suggest(cleanWord);
            if (suggestions.length) {
                const correctedWord = word.replace(cleanWord, suggestions[0]);
                correctedWords += correctedWord;
                asteriskText += '*'.repeat(word.length) + (i < words.length - 1 ? ' ' : '');
            } else {
                correctedWords += word;
                asteriskText += '*'.repeat(word.length) + (i < words.length - 1 ? ' ' : '');
            }
        } else {
            correctedWords += word;
            asteriskText += word;
        }
    }

    const result = {
        correctedText: correctedWords,
        asteriskText: asteriskText.trim(),
        wrongWords
    };

    spellingCache.set(cacheKey, result);

    updateCorrections(result.correctedText, result.asteriskText, result.wrongWords, isPartial, fullText);
    addLogEntry(`Spelling checked (${wrongWordCount} issues)`);
    alert(`Found ${wrongWordCount} misspelled word(s) in the ${isPartial ? 'selected text' : 'entire text'}.`);
}

// Update corrections UI and state
function updateCorrections(correctedText, asteriskText, wrongWords, isPartial, fullText) {
    state.correctedText = correctedText;
    state.asteriskText = asteriskText;
    state.wrongWords = wrongWords;
    state.fullCorrectedText = isPartial
        ? fullText.substring(0, state.selectionStart) + correctedText + fullText.substring(state.selectionEnd)
        : correctedText;
    elements.correctionsArea.value = asteriskText;
    elements.showCorrectedBtn.style.display = wrongWords.length ? 'inline-block' : 'none';
    elements.showWrongBtn.style.display = wrongWords.length ? 'inline-block' : 'none';
    elements.updateBtn.style.display = wrongWords.length ? 'inline-block' : 'none';
    state.isWrongWordsVisible = false;
    elements.showWrongBtn.textContent = 'Show Wrong Words';
}

// Reset corrections UI
function resetCorrections() {
    elements.correctionsArea.value = '';
    elements.showCorrectedBtn.style.display = 'none';
    elements.showWrongBtn.style.display = 'none';
    elements.updateBtn.style.display = 'none';
    state.isWrongWordsVisible = false;
    state.fullCorrectedText = '';
}

// Toggle corrected text visibility
function toggleCorrected() {
    state.isCorrectedVisible = !state.isCorrectedVisible;
    state.isWrongWordsVisible = false;
    elements.showWrongBtn.textContent = 'Show Wrong Words';
    elements.correctionsArea.value = state.isCorrectedVisible ? state.correctedText : state.asteriskText;
    elements.showCorrectedBtn.textContent = state.isCorrectedVisible ? 'Hide Corrected' : 'Show Corrected';
}

// Toggle misspelled words
function toggleWrongWords() {
    state.isWrongWordsVisible = !state.isWrongWordsVisible;
    if (state.isWrongWordsVisible) {
        if (state.wrongWords.length) {
            const asteriskCount = (state.asteriskText.match(/\*/g) || []).length;
            elements.correctionsArea.value = `Number of asterisks (misspelled characters): ${asteriskCount}\n\n${state.wrongWords.join('\n')}`;
        } else {
            elements.correctionsArea.value = 'No misspelled words found.';
        }
        elements.showCorrectedBtn.style.display = 'none';
        elements.showWrongBtn.textContent = 'Hide Wrong Words';
    } else {
        elements.correctionsArea.value = state.isCorrectedVisible ? state.correctedText : state.asteriskText;
        elements.showCorrectedBtn.style.display = state.wrongWords.length ? 'inline-block' : 'none';
        elements.showWrongBtn.textContent = 'Show Wrong Words';
    }
}

// Compute word-level differences
function getWordDiff(original, corrected) {
    const originalWords = original.split(/(\s+)/);
    const correctedWords = corrected.split(/(\s+)/);
    const diff = [];

    for (let i = 0; i < Math.max(originalWords.length, correctedWords.length); i++) {
        const origWord = originalWords[i] || '';
        const corrWord = correctedWords[i] || '';
        if (origWord !== corrWord) {
            diff.push({ index: i, original: origWord, corrected: corrWord });
        }
    }

    return diff;
}

// Show update confirmation with diff
function showUpdateConfirmation() {
    if (!elements.correctionsArea.value || !state.correctedText) return;

    const originalText = elements.editor.value;
    const newText = state.fullCorrectedText;

    const originalLines = originalText.split('\n');
    const newLines = newText.split('\n');
    let diffHTML = '<strong>Changes to be applied:</strong><br><table>';

    for (let i = 0; i < Math.max(originalLines.length, newLines.length); i++) {
        const original = originalLines[i] || '';
        const corrected = newLines[i] || '';
        let lineStyle = '';
        let originalDisplay = original;
        let correctedDisplay = corrected;

        if (original !== corrected) {
            lineStyle = 'background: #ffa6a644;';
            const wordDiff = getWordDiff(original, corrected);
            originalDisplay = original.split(/(\s+)/).map((word, idx) => {
                const diffEntry = wordDiff.find(d => d.index === idx && d.original === word);
                return diffEntry ? `<span style="background: red; color: white;">${word}</span>` : word;
            }).join('');
            correctedDisplay = corrected.split(/(\s+)/).map((word, idx) => {
                const diffEntry = wordDiff.find(d => d.index === idx && d.corrected === word);
                return diffEntry ? `<span style="background: green; color: white;">${word}</span>` : word;
            }).join('');
        }

        diffHTML += `
            <tr style="${lineStyle}">
                <td style="padding: 5px; color: black;">${i + 1}</td>
                <td style="padding: 5px;">${originalDisplay || '[empty]'}</td>
            </tr>`;
        if (original !== corrected) {
            diffHTML += `
                <tr style="background: #a6ffa644;">
                    <td style="padding: 5px; color: black;">${i + 1}</td>
                    <td style="padding: 5px;">${correctedDisplay || '[empty]'}</td>
                </tr>`;
        }
    }

    diffHTML += '</table>';
    elements.diffArea.innerHTML = diffHTML;
    elements.diffArea.style.display = 'block';
    elements.confirmationButtons.style.display = 'inline-block';
    elements.updateBtn.style.display = 'none';
}

// Update from file
// async function updateFromFile() {
//     try {
//         const response = await fetch('newstuff.txt');
//         if (!response.ok) throw new Error('File not found');
//         const text = await response.text();
//         state.correctedText = text;
//         state.asteriskText = text;
//         state.fullCorrectedText = text;
//         state.updateSource = 'file';
//         elements.correctionsArea.value = text;
//         elements.showCorrectedBtn.style.display = 'none';
//         elements.showWrongBtn.style.display = 'none';
//         elements.updateBtn.style.display = 'inline-block';
//         showUpdateConfirmation();
//         addLogEntry('File updated');
//     } catch (err) {
//         alert(`Error loading file: ${err.message}`);
//     }
// }

async function updateFromFile() {
    console.log('updateFromFile called');
    if (window.DOCUMENT_ID === null || window.DOCUMENT_ID === undefined) {
        console.error('Cannot update: DOCUMENT_ID is not defined');
        alert('Error updating document: Document ID is not defined');
        return;
    }
    try {
        const response = await fetch(`/api/docs/${DOCUMENT_ID}/`);
        if (!response.ok) throw new Error(`Server responded ${response.status}`);
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        const text = data.content; // Extract content from JSON
        state.correctedText = text;
        state.asteriskText = text;
        state.fullCorrectedText = text;
        state.updateSource = 'file';
        if (elements.correctionsArea) {
            elements.correctionsArea.value = text;
        } else {
            console.error('Corrections area element not found');
        }
        if (elements.showCorrectedBtn) {
            elements.showCorrectedBtn.style.display = 'none';
        }
        if (elements.showWrongBtn) {
            elements.showWrongBtn.style.display = 'none';
        }
        if (elements.updateBtn) {
            elements.updateBtn.style.display = 'inline-block';
        }
        showUpdateConfirmation();
        addLogEntry('File updated');
        alert('Document updated successfully!');
    } catch (err) {
        console.error('Update failed', err);
        alert(`Error updating document: ${err.message}`);
    }
}

// Confirm text update
function confirmUpdate() {
    elements.editor.value = state.fullCorrectedText;
    resetState();
    addLogEntry('Text updated');
}

// Cancel update
function cancelUpdate() {
    elements.diffArea.style.display = 'none';
    elements.confirmationButtons.style.display = 'none';
    elements.updateBtn.style.display = state.wrongWords.length ? 'inline-block' : 'none';
    state.updateSource = 'spelling';
    state.selectionStart = 0;
    state.selectionEnd = 0;
}

// Reset state and UI
function resetState() {
    elements.correctionsArea.value = '';
    elements.showCorrectedBtn.style.display = 'none';
    elements.showWrongBtn.style.display = 'none';
    elements.updateBtn.style.display = 'none';
    elements.diffArea.style.display = 'none';
    elements.confirmationButtons.style.display = 'none';
    state = {
        correctedText: '',
        asteriskText: '',
        wrongWords: [],
        isCorrectedVisible: false,
        isWrongWordsVisible: false,
        updateSource: 'spelling',
        selectionStart: 0,
        selectionEnd: 0,
        fullCorrectedText: ''
    };
    spellingCache.clear();
}

// Share text to clipboard
async function shareText() {
    try {
        await navigator.clipboard.writeText(elements.editor.value);
        addLogEntry('Text shared');
        alert('Text copied to clipboard for sharing!');
    } catch (err) {
        console.error('Share failed:', err);
    }
}

// Save text to localStorage
function saveText() {
    localStorage.setItem('savedText', elements.editor.value);
    addLogEntry('Text saved');
    alert('Text saved!');
}

// Add collaborator (placeholder)
function addCollaborator() {
    addLogEntry('Collaborator added');
    alert('Add collaborator feature not yet implemented.');
}

// User dropdown functions
function openSettings() {
    addLogEntry('Settings opened');
    alert('Settings feature not yet implemented.');
}

function logout() {
    addLogEntry('User logged out');
    alert('Logout feature not yet implemented.');
}

// Log activity with limit
function addLogEntry(message) {
    const entry = document.createElement('p');
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    elements.activityLog.prepend(entry);
    while (elements.activityLog.children.length > 10) {
        elements.activityLog.removeChild(elements.activityLog.lastChild);
    }
}

// Debounced input handler
const handleInput = debounce(() => {
    resetState();
    updateTokenCount();
}, 300);

/**
 * Read the editor text and POST it to the Django API,
 * then update the “Last Saved” timestamp in the UI.
 * 
 * BAD FUNCTIONALITY REMEMBER TO FIX THIS FETCH OK???
 * 
 * TODO: Impliment Collaborator to update this function properly for warnings
 */

/*
Anthony changes
added getcookie function


*/

// Helper to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function storeToDB() {
    const content = elements.editor.value;
    try {
      const res = await fetch(`/api/docs/${DOCUMENT_ID}/save/`, {
        method: 'POST',
        credentials: 'same-origin',             // include cookies
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),// use your CSRF helper
        },
        body: JSON.stringify({ content }),
      });
  
      if (!res.ok) throw new Error(`Server responded ${res.status}`);
      const data = await res.json();
      
      // reflect the new timestamp
      elements.lastSaved.textContent =
        'Last Saved: ' + new Date(data.latest_update).toLocaleString();
      addLogEntry('Saved to DB');
      alert('Document saved successfully!');
    } catch (err) {
      console.error('Save failed', err);
      alert(`Error saving document: ${err.message}`);
    }
  }
  

// Event listeners
elements.editor.addEventListener('input', handleInput);
elements.themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    elements.themeToggleBtn.textContent = isDark ? 'Light Theme' : 'Dark Theme';
});

elements.userPic.addEventListener('click', () => {
    elements.userDropdown.classList.toggle('active');
});

elements.hamburgerBtn.addEventListener('click', () => {
    elements.navLinks.classList.toggle('active');
    elements.hamburgerBtn.classList.toggle('active');
});

elements.updateFromDbBtn.addEventListener('click', updateFromFile)
elements.saveToDbBtn.addEventListener('click', storeToDB)


// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!elements.userMenu.contains(e.target)) {
        elements.userDropdown.classList.remove('active');
    }
    if (!elements.navLinks.contains(e.target) && !elements.hamburgerBtn.contains(e.target)) {
        elements.navLinks.classList.remove('active');
        elements.hamburgerBtn.classList.remove('active');
    }
});

// Initialize theme and token count
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-theme');
        elements.themeToggleBtn.textContent = 'Light Theme';
    }
    updateTokenCount();
});