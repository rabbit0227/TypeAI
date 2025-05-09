// Spelling check and correction logic
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