# Imports
import google.generativeai as genai
from PIL import Image
import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for, jsonify, send_file
from pdf2image import convert_from_path
load_dotenv()

# Flask app configurations
app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Gemini_API_KEY config
GOOGLE_API_KEY = os.getenv("API_KEY")
genai.configure(api_key = GOOGLE_API_KEY)

# Gemini model selection
textModel = genai.GenerativeModel('gemini-pro')
visionModel = genai.GenerativeModel('gemini-pro-vision')

# --> PDF2Image

# path of pdf 
# pdfPath = r"./essayPdf/Course Plan Eng Phy.pdf"

def pdfToText(pdfPath):
	poppler_path = os.getenv("PopplerPath")
	pages =convert_from_path(pdf_path= pdfPath, poppler_path = poppler_path)
	#path to save the output in
	saving_folder = r"./essayImages/"

	text = ""
	#to count the number of pages
	counter = 1
	#iterateover all the pages of the pdf
	for page in pages:
		img_name = f"Page_{counter}.png"
		path = os.path.join(saving_folder,img_name)
		page.save(path, "PNG")
		img = Image.open(path)
		textResponse = visionModel.generate_content(["Extract all the text that you see in this image, do not add new things, be accurate.", img], stream=True)
		textResponse.resolve()
		# print(textResponse.text)
		text += textResponse.text
		counter += 1

	return text

def analyseText(text, refStr):
	response = textModel.generate_content("Given is an essay written by a student, analyze it and give constructive feedback and score out it out of 10 marks. After the generation of the entire analysis, write a separate last line which has Marks:X/10, in exactly the same format so that we can apply regular expressions to extract the value of marks later on(The Marks:X/10 field at last is compulsory, don't miss it at any cost). The topic is: " + refStr + " and the text is "+ text)
	# with open(r'./analysisText/output.txt', 'w+') as fp:
	# 	fp.write(response.text)

	return response.text

def preprocessFeedback(feedback):
    # Check and remove the "Score: Marks:" part if it exists at the end of the feedback
    score_prefix = "*Score: Marks:"
    if score_prefix in feedback:
        feedback = feedback[:feedback.rfind(score_prefix)].strip()

    # Splitting the feedback into parts for formatting
    parts = feedback.split("*")
    cleaned_parts = [part.strip() for part in parts if part]

    # Constructing an HTML list for the feedback
    feedback_html = "<ul>"
    for part in cleaned_parts:
        if part:  # Ensure part is not empty
            # Check if part is a title like 'Analysis:', 'Constructive Feedback:'
            if part.endswith(":"):
                feedback_html += f"<li><strong>{part}</strong></li>"
            else:
                feedback_html += f"<li>{part}</li>"
    feedback_html += "</ul>"
    return feedback_html

def generateHTMLOutput(analysedData):
    # Assuming analysedData is a single string formatted as "Roll Number, Marks Obtained, Feedback"
    parts = analysedData.split(',')
    roll_number = parts[0].strip()
    marks_obtained = parts[1].strip()
    feedback = ','.join(parts[2:]).strip()  # Join back in case feedback contains commas
    
    formatted_feedback = preprocessFeedback(feedback)
    
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {{
      font-family: Arial, sans-serif;
      border-collapse: collapse;
      width: 50%;
    }}

    td, th {{
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }}

    th {{
      background-color: #f2f2f2;
    }}

    ul {{
      list-style-type: none;
      padding: 0;
    }}

    ul li {{
      padding: 2px;
    }}

    ul li strong {{
      font-weight: bold;
    }}
    </style>
    </head>
    <body>

    <h2>Student Marks</h2>

    <table>
      <tr>
        <th>Roll Number</th>
        <th>Marks Obtained</th>
        <th>Remarks or Comments</th>
      </tr>
      <tr>
        <td>{roll_number}</td>
        <td>{marks_obtained}</td>
        <td>{formatted_feedback}</td>
      </tr>
    </table>

    </body>
    </html>
    '''
    return html_content

def filterFields(analysedText, pdfPath):
	patternRollNo = r"(?<=-)\w+(?=\.)"
	patternMarks = r"(\d+/\d+)"
	matchRollNo = re.search(patternRollNo, pdfPath)
	matchMarks = re.findall(patternMarks, analysedText)
	if matchRollNo:
		roll_number = matchRollNo.group()
	if matchMarks:
		marks = matchMarks[-1]
	review = re.sub(patternMarks, "", analysedText)

	analysis_data = f"{roll_number}, {marks}, {review}"

	return analysis_data


# pdfPath = r"./essayPdf/IndianEconomics-23WU0102100.pdf"
# essayText = pdfToText(pdfPath)
# analysed = analyseText(essayText, "Indian Economics")
# # Generate HTML output
# print(analysed)
# html_output = generateHTMLOutput(filterFields(analysed, pdfPath))
# # Write HTML output to a file
# with open("./outputHTML/student_marks.html", "w") as file:
#     file.write(html_output)

# Sample implementation of LLM API to generate analysis of text
# essayText = "Technology has become an integral part of our lives, transforming the way we live, work, and communicate. From smartphones and laptops to smart homes and self-driving cars, technology has made our lives more convenient and efficient. It has also opened up new opportunities for innovation, creativity, and economic growth. However, as with any powerful tool, technology also presents challenges, such as privacy concerns, cybersecurity threats, and the potential for job displacement. As we continue to navigate this rapidly evolving landscape, it is important to approach technology with a critical and informed perspective, considering both its benefits and its potential risks."

# path = os.path.join(r"./essayImages/", "Page_1.png")
# img = Image.open(path)
# textResponse = visionModel.generate_content(["Extract all the text that you see in this image, do not add new things, be accurate.", img], stream=True)
# textResponse.resolve()
# print(textResponse.text)  --> Helped in Logic Building


# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'

# dictionary to store user and password
users = {
	'user1': 'password1',
	'user2': 'password2'
}

# To render a login form 
@app.route('/')
def home():
	return render_template('index.html')

# Login logic
@app.route('/login', methods=['POST'])
def login():
		username = request.form['username']
		password = request.form['password']
		if username in users and users[username] == password:
			return redirect(url_for('upload'))
		else:
			return render_template('index.html', message="Login failed. Please check your credentials and try again.")

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods = ['POST'])
def upload():
	if request.method == 'POST':
			uploaded_file = request.files['pdfFile']
			print('file uploaded')
			pdfPath = './temp/' + uploaded_file.filename
			with open(pdfPath, 'wb') as file:
				file.write(uploaded_file.read())

			prompt = request.form['prompt']

			essayText = pdfToText(pdfPath)
			analysed = analyseText(essayText, prompt)
			html_output = generateHTMLOutput(filterFields(analysed, pdfPath))
			with open("./outputHTML/student_marks.html", "w") as file:
				file.write(html_output)

			
			
			# <---> Logic for accepting pdf input and converting it into text, that is, essayText would hold a String

		# essayText = "Technology has become an integral part of our lives, transforming the way we live, work, and communicate. From smartphones and laptops to smart homes and self-driving cars, technology has made our lives more convenient and efficient. It has also opened up new opportunities for innovation, creativity, and economic growth. However, as with any powerful tool, technology also presents challenges, such as privacy concerns, cybersecurity threats, and the potential for job displacement. As we continue to navigate this rapidly evolving landscape, it is important to approach technology with a critical and informed perspective, considering both its benefits and its potential risks."
		# response = textModel.generate_content("Given is an essay written by a student, analyze it and give constructive feedback and score out it out of 10 marks. The topic is: " + "Technology" + essayText)
		# with open(r'./analysisText/output.txt', 'w+') as fp:
		# 	fp.write(response.text)
		# return 'Done!'
				
# @app.route('/path_to_your_html')
# def serve_html():
#     # Logic to serve your HTML content
#     # For example, reading from a file and returning its contents
#     with open('./outputHTML/student_marks.html', 'r') as file:
#         html_content = file.read()
#     return html_content





if __name__ == '__main__':
	app.run(debug=True)