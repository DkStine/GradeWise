document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.getElementById('uploadForm');
  const promptInput = document.querySelector('.text-prompt'); // Access the text prompt input

  uploadForm.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    // Trim the input and check if it's empty
    const promptText = promptInput.value.trim();
    if (promptText === '') {
      alert('Please specify a topic in the prompt input box.');
      return; // Prevent the form from being submitted
    }

    const formData = new FormData();
    const filesInput = document.querySelector('input[type="file"]');
    
    // Loop through each file selected and add to FormData
    for (let i = 0; i < filesInput.files.length; i++) {
      formData.append('pdfFile', filesInput.files[i]); // Changed from 'files[]' to 'pdfFile'
    }

    // Optionally add the prompt text to formData for server-side processing
    formData.append('prompt', promptText);

    // Use fetch to send the request to the Flask server
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