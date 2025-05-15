document.addEventListener('DOMContentLoaded', function() {
    // Message type selector functionality
    const typeOptions = document.querySelectorAll('.message-type-option');
    const messageTypeInput = document.getElementById('message_type');
    const documentSelector = document.getElementById('document-selector');
    
    // Function to set active message type
    function setActiveMessageType(messageType) {
        // Remove active class from all options
        typeOptions.forEach(opt => opt.classList.remove('active'));
        
        // Add active class to relevant option
        document.querySelector(`.message-type-${messageType.toLowerCase()}`).classList.add('active');
        
        // Update hidden input value
        messageTypeInput.value = messageType;
        
        // Show/hide document selector based on message type
        if (messageType === 'Collaboration') {
            documentSelector.style.display = 'block';
        } else {
            documentSelector.style.display = 'none';
        }
        
        // Update subject placeholder based on message type
        const subjectField = document.getElementById('id_subject');
        if (messageType === 'Collaboration') {
            subjectField.placeholder = 'Collaboration invitation for document';
        } else if (messageType === 'Complaint') {
            subjectField.placeholder = 'Issue report for administrator';
        } else {
            subjectField.placeholder = 'Message subject';
        }
    }
    
    // Click event handlers for message type options
    typeOptions.forEach(option => {
        option.addEventListener('click', function() {
            const messageType = this.getAttribute('data-type');
            setActiveMessageType(messageType);
        });
    });
    
    // Check if we should activate a specific tab
    // First check if the server provided an active_tab in the context
    const activeTabFromServer = '{{ active_tab|default:"" }}';
    
    if (activeTabFromServer) {
        // Use the tab provided by the server view
        setActiveMessageType(activeTabFromServer);
    } else {
        // Otherwise, check URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const typeParam = urlParams.get('type');
        
        if (typeParam) {
            // Capitalize first letter for matching the data-type attribute
            const messageType = typeParam.charAt(0).toUpperCase() + typeParam.slice(1);
            setActiveMessageType(messageType);
        } else {
            // Set Regular as default (already set in HTML)
            setActiveMessageType('Regular');
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Message type selector functionality
    const typeOptions = document.querySelectorAll('.message-type-option');
    const messageTypeInput = document.getElementById('message_type');
    const documentSelector = document.getElementById('document-selector');
    
    typeOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            typeOptions.forEach(opt => opt.classList.remove('active'));
            
            // Add active class to clicked option
            this.classList.add('active');
            
            // Update hidden input value
            const messageType = this.getAttribute('data-type');
            messageTypeInput.value = messageType;
            
            // Show/hide document selector based on message type
            if (messageType === 'Collaboration') {
                documentSelector.style.display = 'block';
            } else {
                documentSelector.style.display = 'none';
            }
            
            // Update subject placeholder based on message type
            const subjectField = document.getElementById('id_subject');
            if (messageType === 'Collaboration') {
                subjectField.placeholder = 'Collaboration invitation for document';
            } else if (messageType === 'Complaint') {
                subjectField.placeholder = 'Issue report for administrator';
            } else {
                subjectField.placeholder = 'Message subject';
            }
        });
    });
});