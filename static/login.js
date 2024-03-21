document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
  
    togglePassword.addEventListener('click', function(e) {
      // Toggle the type attribute
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      
      // Toggle the eye icon
      this.classList.toggle('fa-eye-slash');
    });
  
    // Existing form submission handling code...
    const uploadForm = document.getElementById('uploadForm');
  
    uploadForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent the default form submission
      
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      
      fetch('/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded', // Use form data content type
          },
          body: new URLSearchParams({
              'username': username,
              'password': password
          }),
      })
      .then(response => {
          if (response.ok) {
              window.location.href = "/upload";
          } else {
              alert("Login failed. Please check your credentials and try again.");
          }
      });
    });
  });
  