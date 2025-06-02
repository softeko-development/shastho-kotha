document.getElementById('dark-mode').addEventListener('change', function() {
    var isChecked = this.checked;
    var doctorId = this.getAttribute('data-id'); // Fetch doctor ID from data-id attribute
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // Get CSRF token
    console.log(doctorId)
    fetch(`/update-working-status/${doctorId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Include CSRF token
        },
        body: JSON.stringify({ working_status: isChecked })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Working status updated successfully.");
        } else {
            console.log("Failed to update working status.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
