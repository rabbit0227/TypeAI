/* note from David, fileJS.js is already 400+ lines and my DOM cache content are not loading
   all related function for inboxing and messaging will be added here and linked to their respective html*/


document.addEventListener('DOMContentLoaded', function () {
    // For switching tabs (sent and received), will set active flag and hide/load content
    const elements = {
        tabs: document.querySelectorAll('.inbox-tab'),
        contentSections: document.querySelectorAll('.inbox-content'),
    };

    elements.tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            elements.tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            elements.contentSections.forEach(section => section.classList.remove('active'));

            const tabName = tab.getAttribute('data-tab');
            const content = document.getElementById(`${tabName}-content`);
            if (content) content.classList.add('active');
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // purely for the notification on inbox icon, will fetch data calculated by inbox for new mail
    function updateUnreadCount() {
        const unreadBadge = document.getElementById('unreadBadge');
        if (unreadBadge) {
            fetch('/inbox/unread-count/') 
                .then(response => response.json())
                .then(data => {
                    const count = data.unread_count;
                    unreadBadge.textContent = count;

                    if (count <= 0) {
                        unreadBadge.style.display = 'none';
                    } else {
                        unreadBadge.style.display = 'flex';
                    }
                })
                .catch(error => console.error('Error fetching unread count:', error));
        }
    }

    updateUnreadCount();
    setInterval(updateUnreadCount, 60000); // update time accordingly, this will auto run on bootup
});


/*
document.addEventListener('DOMContentLoaded', function() {
    
    const inboxBtn = document.getElementById('inboxBtn');
    const unreadUrl = inboxBtn ? inboxBtn.getAttribute('data-unread-url') : null;
    
    function updateUnreadCount() {
        const unreadBadge = document.getElementById('unreadBadge');
        if (unreadBadge && unreadUrl) {
            fetch(unreadUrl)
                .then(response => response.json())
                .then(data => {
                    const count = data.unread_count;
                    unreadBadge.textContent = count;
    
                    if (count <= 0) {
                        unreadBadge.style.display = 'none';
                    } else {
                        unreadBadge.style.display = 'flex';
                    }
                })
                .catch(error => console.error('Error fetching unread count:', error));
        }
    }
});
*/