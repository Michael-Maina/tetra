const body = document.querySelector("body"),
sidebar = body.querySelector(".sidebarbody"),
toggle = body.querySelector(".toggle"),
modeSwitch = body.querySelector(".toggle-switch"),
modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () =>{
    sidebar.classList.toggle("close");
});

modeSwitch.addEventListener("click", () =>{
    body.classList.toggle("dark");

    if(body.classList.contains("dark")){
        modeText.innerText = "Light Mode"
    }else{
        modeText.innerText = "Dark Mode"
    }
});


// script.js

document.addEventListener('DOMContentLoaded', function () {
    // Get references to the sections
    const dashboardSection = document.querySelector('.home');
    const calendarSection = document.querySelector('.calendar');
    const microphoneSection = document.querySelector('.microphone');
    const chatSection = document.querySelector('.chat');

    // Get references to the sidebar links
    const homeLink = document.querySelector('.nav-link:nth-child(1) a');
    const calendarLink = document.querySelector('.nav-link:nth-child(2) a');
    const microphoneLink = document.querySelector('.nav-link:nth-child(3) a');
    const chatLink = document.querySelector('.nav-link:nth-child(4) a');

    // Function to hide all sections
    function hideAllSections() {
        dashboardSection.style.display = 'none';
        calendarSection.style.display = 'none';
        microphoneSection.style.display = 'none';
        chatSection.style.display = 'none';
    }

    // Initially hide all sections except the dashboard
    hideAllSections();
    dashboardSection.style.display = 'block';

    // Event listeners for sidebar links
    homeLink.addEventListener('click', () => {
        hideAllSections();
        dashboardSection.style.display = 'block';
    });

    calendarLink.addEventListener('click', () => {
        hideAllSections();
        calendarSection.style.display = 'block';
    });

    microphoneLink.addEventListener('click', () => {
        hideAllSections();
        microphoneSection.style.display = 'block';
    });

    chatLink.addEventListener('click', () => {
        hideAllSections();
        chatSection.style.display = 'block';
    });
});



// Add your Google Calendar API integration here

// Sample data (replace with your actual data)
const sampleEvents = [
    { summary: 'Event 1', start: '2023-11-30T10:00:00Z' },
    { summary: 'Event 2', start: '2023-12-01T15:30:00Z' },
    // Add more events as needed
];

function renderEvents(events) {
    const eventsList = document.getElementById('events-list');
    eventsList.innerHTML = '';

    events.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.classList.add('event');
        eventElement.innerHTML = `<strong>${event.summary}</strong><br>${new Date(event.start).toLocaleString()}`;
        eventsList.appendChild(eventElement);
    });
}

// Call the Google Calendar API and pass the received events to renderEvents function
// Replace this with your actual API call
renderEvents(sampleEvents);
