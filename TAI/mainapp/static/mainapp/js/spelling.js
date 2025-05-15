async function checkSpelling() {
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
        const { correctedText, asteriskText, wrongWords, blacklistedWords } = spellingCache.get(cacheKey);
        state.wrongWords = wrongWords; // Store in state
        state.blacklistedWords = blacklistedWords; // Store in state
        updateCorrections(correctedText, asteriskText, wrongWords, isPartial, fullText);
        alert(`Found ${wrongWords.length} misspelled word(s) and ${blacklistedWords.length} blacklisted word(s).`);
        return;
    }

    try {
        // Fetch blacklist from Django API
        const blacklistResponse = await fetch('/api/blacklist/', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });
        if (!blacklistResponse.ok) throw new Error('Failed to fetch blacklist');
        const blacklistData = await blacklistResponse.json();
        const blacklist = blacklistData.black_lsit_words.map(item => item.word.toLowerCase());

        const words = textToCheck.split(/(\s+)/);
        let correctedWords = '';
        let asteriskText = '';
        const wrongWords = [];
        const blacklistedWords = [];
        let wrongWordCount = 0;
        let blacklistCount = 0;

        for (let i = 0; i < words.length; i++) {
            const word = words[i];
            const isWhitespace = /\s+/.test(word);
            const cleanWord = word.replace(/[.,!?]/g, '').toLowerCase();

            if (!isWhitespace && cleanWord) {
                if (blacklist.includes(cleanWord)) {
                    blacklistCount++;
                    blacklistedWords.push(cleanWord);
                    correctedWords += word; // Keep original blacklisted word
                    asteriskText += '*'.repeat(word.length);
                } else if (!dictionary.check(cleanWord)) {
                    wrongWordCount++;
                    wrongWords.push(cleanWord);
                    const suggestions = dictionary.suggest(cleanWord);
                    if (suggestions.length) {
                        const correctedWord = word.replace(cleanWord, suggestions[0]);
                        correctedWords += correctedWord;
                        asteriskText += '*'.repeat(word.length);
                    } else {
                        correctedWords += word;
                        asteriskText += '*'.repeat(word.length);
                    }
                } else {
                    correctedWords += word;
                    asteriskText += word;
                }
            } else {
                correctedWords += word;
                asteriskText += word;
            }
            if (!isWhitespace && i < words.length - 1) {
                asteriskText += ' ';
            }
        }

        // Prepare data for Django text correction function
        const correctionData = {
            input_text: textToCheck,
            hidden_text: asteriskText.trim(),
            blacklist_words: blacklistedWords
        };

        // Call Django text correction API
        const correctionResponse = await fetch('/api/correct-text/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(correctionData),
        });

        if (!correctionResponse.ok) throw new Error('Text correction failed');
        const correctionResult = await correctionResponse.json();
        const correctedText = correctionResult.corrected_text;

        const result = {
            correctedText: correctedText,
            asteriskText: asteriskText.trim(),
            wrongWords,
            blacklistedWords
        };

        spellingCache.set(cacheKey, result);
        state.wrongWords = wrongWords; // Store in state
        state.blacklistedWords = blacklistedWords; // Store in state

        updateCorrections(correctedText, asteriskText.trim(), wrongWords, isPartial, fullText);
        addLogEntry(`Spelling checked (${wrongWordCount} misspelled, ${blacklistCount} blacklisted)`);
        alert(`Found ${wrongWordCount} misspelled word(s) and ${blacklistCount} blacklisted word(s).`);
    } catch (error) {
        console.error('Error in checkSpelling:', error);
        alert('An error occurred while checking spelling.');
    }
}

// Helper function to get CSRF token
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