// State management for application data
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