// Database operations
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