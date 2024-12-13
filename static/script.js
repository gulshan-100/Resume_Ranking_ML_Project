// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const jobDescriptionInput = document.getElementById('job_description');
    const degreeInput = document.getElementById('degree');
    const experienceInput = document.getElementById('experience');

    form.addEventListener('submit', function(event) {
        // Basic validation
        if (!jobDescriptionInput.value.trim()) {
            alert('Please enter a job description.');
            event.preventDefault();
            return;
        }

        if (!degreeInput.value.trim()) {
            alert('Please enter a degree.');
            event.preventDefault();
            return;
        }

        if (!experienceInput.value || experienceInput.value < 0) {
            alert('Please enter a valid number of years for experience.');
            event.preventDefault();
            return;
        }
    });
});