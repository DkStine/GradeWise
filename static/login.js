document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
  
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
  
        // Retrieve user input
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
  
        // Create FormData object and append credentials
        let formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        // Send an AJAX request to your Flask backend
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle response from Flask
            console.log(data); // For debugging purposes
            if (data.success) {
                // Redirect to the upload page if login is successful
                window.location.href = 'upload.html'; // Change this URL to your upload page's URL
            } else {
                // Alert the user if login failed
                alert('Login failed: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
  });


document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...

    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    togglePassword.addEventListener('click', function(e) {
        // Toggle the type attribute using a ternary operator
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        // Toggle the icon class
        this.classList.toggle('fa-eye-slash');
    });

});
  