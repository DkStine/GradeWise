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
              window.location.href = '/dashboard'; // Redirect to dashboard if login is successful
          } else {
              alert('Login failed: ' + data.message); // Show error message
          }
      })
      .catch(error => console.error('Error:', error));
  });
});
