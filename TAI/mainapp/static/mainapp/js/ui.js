// UI update and interaction functions
function updateTokenCount() {
    const text = elements.editor.value;
    const usedTokens = text.trim() ? text.split(/\s+/).length : 0;
    const maxTokens = 1000; // Example max tokens
    elements.usedTokens.textContent = `Used Tokens: ${usedTokens}`;
    elements.availableTokens.textContent = `Available Tokens: ${maxTokens - usedTokens}`;
}

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

function resetCorrections() {
    elements.correctionsArea.value = '';
    elements.showCorrectedBtn.style.display = 'none';
    elements.showWrongBtn.style.display = 'none';
    elements.updateBtn.style.display = 'none';
    state.isWrongWordsVisible = false;
    state.fullCorrectedText = '';
}

function toggleCorrected() {
    state.isCorrectedVisible = !state.isCorrectedVisible;
    state.isWrongWordsVisible = false;
    elements.showWrongBtn.textContent = 'Show Wrong Words';
    elements.correctionsArea.value = state.isCorrectedVisible ? state.correctedText : state.asteriskText;
    elements.showCorrectedBtn.textContent = state.isCorrectedVisible ? 'Hide Corrected' : 'Show Corrected';
}

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

function confirmUpdate() {
    elements.editor.value = state.fullCorrectedText;
    resetState();
    addLogEntry('Text updated');
}

function cancelUpdate() {
    elements.diffArea.style.display = 'none';
    elements.confirmationButtons.style.display = 'none';
    elements.updateBtn.style.display = state.wrongWords.length ? 'inline-block' : 'none';
    state.updateSource = 'spelling';
    state.selectionStart = 0;
    state.selectionEnd = 0;
}

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

function addLogEntry(message) {
    const entry = document.createElement('p');
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    elements.activityLog.prepend(entry);
    while (elements.activityLog.children.length > 10) {
        elements.activityLog.removeChild(elements.activityLog.lastChild);
    }
}