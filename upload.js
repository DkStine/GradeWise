document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.getElementById('uploadForm');

  uploadForm.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission
    
    const formData = new FormData();
    const filesInput = document.querySelector('input[type="file"]');
    
    // Loop through each file selected and add to FormData
    for (let i = 0; i < filesInput.files.length; i++) {
      formData.append('files[]', filesInput.files[i]);
    }

    // Use `fetch` to send the request to the Flask server
    fetch('/upload', {
      method: 'POST',
      body: formData, // FormData will be used in the body of the request
    })
    .then(response => response.json()) // Assuming the server responds with JSON
    .then(data => {
      console.log(data); // Handle the response data
    })
    .catch(error => {
      console.error(error); // Handle any errors
    });
  });
});
