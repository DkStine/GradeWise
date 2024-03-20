document.getElementById("loginForm").addEventListener("submit", function(event) {
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
