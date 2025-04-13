// Initialize Typo dictionary
const dictionary = new Typo('en_US', false, false, {
    dictionaryPath: 'https://unpkg.com/typo-js@1.2.4/dictionaries'
});

// Cache DOM elements
const elements = {
    editor: document.getElementById('editor'),
    correctionsArea: document.getElementById('correctionsArea'),
    showCorrectedBtn: document.getElementById('showCorrectedBtn'),
    diffArea: document.getElementById('diffArea'),
    updateBtn: document.getElementById('updateBtn'),
    confirmationButtons: document.getElementById('confirmationButtons'),
    activityLog: document.getElementById('activityLog'),
    themeToggleBtn: document.getElementById('themeToggleBtn')
};

// State management
let state = {
    correctedText: '',
    asteriskText: '',
    wrongWords: [],
    isCorrectedVisible: false,
    updateSource: 'spelling',
    selectionStart: 0,
    selectionEnd: 0,
    fullCorrectedText: '' // Tracks the full text after partial correction
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

// Check spelling for selected or full text
function checkSpelling() {
    const fullText = elements.editor.value;
    state.selectionStart = elements.editor.selectionStart;
    state.selectionEnd = elements.editor.selectionEnd;

    // Determine text to check
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

    // Check cache
    const cacheKey = `${textToCheck}_${state.selectionStart}_${state.selectionEnd}`;
    if (spellingCache.has(cacheKey)) {
        const { correctedText, asteriskText, wrongWords } = spellingCache.get(cacheKey);
        updateCorrections(correctedText, asteriskText, wrongWords, isPartial, fullText);
        return;
    }

    // Split text into words, respecting boundaries
    const words = textToCheck.split(/(\s+)/); // Preserve whitespace
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
                // Replace only the clean word, preserving punctuation
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

    // If partial, reconstruct full text with corrected portion
    const result = {
        correctedText: correctedWords,
        asteriskText: asteriskText.trim(),
        wrongWords
    };

    // Cache results
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
}

// Reset corrections UI
function resetCorrections() {
    elements.correctionsArea.value = '';
    elements.showCorrectedBtn.style.display = 'none';
    state.fullCorrectedText = '';
}

// Toggle corrected text visibility
function toggleCorrected() {
    state.isCorrectedVisible = !state.isCorrectedVisible;
    elements.correctionsArea.value = state.isCorrectedVisible ? state.correctedText : state.asteriskText;
    elements.showCorrectedBtn.textContent = state.isCorrectedVisible ? 'Hide Corrected' : 'Show Corrected';
}

// Show misspelled words
function showWrongWords() {
    if (state.wrongWords.length) {
        const asteriskCount = (state.asteriskText.match(/\*/g) || []).length;
        elements.correctionsArea.value = `Number of asterisks (misspelled characters): ${asteriskCount}\n\n${state.wrongWords.join('\n')}`;
        elements.showCorrectedBtn.style.display = 'none';
    } else {
        elements.correctionsArea.value = 'No misspelled words found.';
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
async function updateFromFile() {
    try {
        const response = await fetch('newstuff.txt');
        if (!response.ok) throw new Error('File not found');
        const text = await response.text();
        state.correctedText = text;
        state.asteriskText = text;
        state.fullCorrectedText = text;
        state.updateSource = 'file';
        elements.correctionsArea.value = text;
        elements.showCorrectedBtn.style.display = 'none';
        showUpdateConfirmation();
        addLogEntry('File updated');
    } catch (err) {
        alert(`Error loading file: ${err.message}`);
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
    elements.updateBtn.style.display = 'inline-block';
    state.updateSource = 'spelling';
    state.selectionStart = 0;
    state.selectionEnd = 0;
}

// Reset state and UI
function resetState() {
    elements.correctionsArea.value = '';
    elements.showCorrectedBtn.style.display = 'none';
    elements.diffArea.style.display = 'none';
    elements.confirmationButtons.style.display = 'none';
    elements.updateBtn.style.display = 'inline-block';
    state = {
        correctedText: '',
        asteriskText: '',
        wrongWords: [],
        isCorrectedVisible: false,
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
}, 300);

// Event listeners
elements.editor.addEventListener('input', handleInput);
elements.themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    elements.themeToggleBtn.textContent = isDark ? 'Light Theme' : 'Dark Theme';
});

// Initialize theme
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-theme');
        elements.themeToggleBtn.textContent = 'Light Theme';
    }
});