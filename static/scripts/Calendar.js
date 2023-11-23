document.addEventListener('DOMContentLoaded', function () {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const monthYearElement = document.getElementById('monthYear');
    const weeksContainer = document.querySelector('.weeks');

    let currentDate = new Date();

    function renderCalendar() {
        const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
        const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
        const daysInMonth = lastDayOfMonth.getDate();

        monthYearElement.textContent = `${getMonthName(currentDate.getMonth())} ${currentDate.getFullYear()}`;
        weeksContainer.innerHTML = '';

        // Render days of the week
        const dayOfWeekNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        for (let i = 0; i < dayOfWeekNames.length; i++) {
            const dayOfWeekElement = document.createElement('li');
            dayOfWeekElement.textContent = dayOfWeekNames[i];
            dayOfWeekElement.classList.add('weeks');
            weeksContainer.appendChild(dayOfWeekElement);
        }

        // Render days
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
            const dayElement = document.createElement('li');
            dayElement.classList.add('days');
            dayElement.textContent = day;

            // Highlight current date
            if (
                date.getDate() === new Date().getDate() &&
                date.getMonth() === new Date().getMonth() &&
                date.getFullYear() === new Date().getFullYear()
            ) {
                dayElement.classList.add('active');
            }

            weeksContainer.appendChild(dayElement);
        }
    }

    function getMonthName(month) {
        const monthNames = [
            'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ];
        return monthNames[month];
    }

    function prevMonth() {
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
        renderCalendar();
    }

    function nextMonth() {
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
        renderCalendar();
    }

    // Event listeners
    prevBtn.addEventListener('click', prevMonth);
    nextBtn.addEventListener('click', nextMonth);

    // Initial rendering
    renderCalendar();
});
