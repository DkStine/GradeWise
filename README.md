# 📈 GradeWise

## Introduction

This project is a web application for analyzing essays submitted by students. It features a frontend built with HTML, CSS, and JavaScript, and a backend developed using Flask and Python.


## Installation

1. Clone the repository and run the following command in the terminal to create the environment:
```bash
pip install -r requirements.txt
```

2. Install `poppler` onto your system from [ @oschwartz10612 version](https://github.com/oschwartz10612/poppler-windows/releases/) and add it to the PATH. (Copy the PATH as well, will tell you why...)

3. Create a `.env` file in the root directory of your project and store the Google API key in the file as `API_KEY = YourAPIKey`, and the path to poppler as `PopplerPath = r'your/path/to/poppler'`

4. Also create a directory named `essayImages` as well in the root directory of the project.

5. Launch the terminal in the project's root directory. Now run `app.py` on the terminal by the following command:
```bash
python app.py
```

6. Go to the `localhost` on which the web app is running and enjoy the application!


## Workflow

* Front-End Development

* Setting Up Flask Backend:
   - Objective: Receive and process files, interact with Gemini API and MongoDB.
   -Receive Files: Setup Flask route for handling POST requests with file data.
   - File Processing: Extract text from typed PDFs, convert handwritten PDFs to images, use regex for student IDs.

* Interaction with Gemini API:
   - Objective: Send data to Gemini, receive feedback and scores.
   -  API Requests: Construct HTTP requests to Gemini API endpoint.
   - Process Response: Parse JSON response for feedback and scores.

* Generating Feedback HTML and Saving Results:
   - Objective: Convert feedback into HTML, save CSV with student IDs and HTML links.
   - HTML Generation: Use Jinja2 for dynamic HTML creation.
   - Save HTML Files: Save to directory with accessible links.
   -  CSV Creation: Track student IDs and links, save using Python's csv module.

* Serving CSV File to Web App:
   - Objective: Enable download of CSV file through web interface.
   - Flask Route for Download: Create route for serving CSV file, set appropriate headers.

* Implementation Overview:
    - Front-End to Flask: JavaScript sends uploaded files to Flask.
    - Flask Processing: Receives, processes files, interacts with Gemini API.
    - Gemini Analysis: Provides feedback and scores, Flask stores data.
    - Feedback Distribution: Web app provides feedback in HTML format to download for teacher access.

### This workflow encompasses front-end, back-end development, API integration, and database management, covering various aspects of web development and data processing.

## Authors

* [Disha Agarwal](https://github.com/disha-a7)
* [KL Rohith](https://github.com/Rohith-Kaki)
* [Shravani A Wanjari](https://github.com/ShravaniAWanjari)
* [Deepak Kumar](https://github.com/DkStine)

###### Project originally created for the HackSavvy 24 Hours Hackathon held at Mahatma Gandhi Institute of Technology, Hyderabad.