function nextPage(pageNumber) {
    document.getElementById(`page${pageNumber - 1}`).style.display = 'none';
    document.getElementById(`page${pageNumber}`).style.display = 'block';
    updateNavigation(pageNumber);
}

function prevPage(pageNumber) {
    document.getElementById(`page${pageNumber + 1}`).style.display = 'none';
    document.getElementById(`page${pageNumber}`).style.display = 'block';
    updateNavigation(pageNumber);
}

function updateNavigation(pageNumber) {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        if (index + 1 === pageNumber) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

document.getElementById('surveyForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Thank you for completing the survey! Your feedback is valuable to us.');
    // You can add code here to send the form data to a server
});