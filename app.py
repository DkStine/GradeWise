# Imports
import google.generativeai as genai
from PIL import Image
import pytesseract
import pathlib
import textwrap
import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo
from pdf2image import convert_from_path
load_dotenv()

# Flask app configurations
app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/model'
mongo = PyMongo(app)

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
	poppler_path = r"C:/Users/91993/Downloads/Programs/Release-24.02.0-0/poppler-24.02.0/Library/bin"
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

def generateHTMLOutput(analysedData):
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
      {analysedData}
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

	analysis_data = f'''
	<tr>
	<td>{roll_number}</td>
	<td>{marks}</td>
	<td>{review}</td>
	
	</tr>
	'''

	return analysis_data


pdfPath = r"./essayPdf/IndianEconomics-23WU0102100.pdf"
essayText = pdfToText(pdfPath)
analysed = analyseText(essayText, "Indian Economics")
# Generate HTML output
print(analysed)
html_output = generateHTMLOutput(filterFields(analysed, pdfPath))
# Write HTML output to a file
with open("./outputHTML/student_marks.html", "w") as file:
    file.write(html_output)

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
	'kunal': '1234',
	'user2': 'password2'
}

# To render a login form 
@app.route('/')
def view_form():
	return render_template('index.html')

# Login logic
@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username in users and users[username] == password:
			return redirect(url_for('input'))
		else:
			return '<p>Login failed</p>'


@app.route('/input', methods = ['POST'])
def input():
	if request.method == 'POST':
			# uploaded_file = request.files['pdfFile']
			# pdfPath = '/tmp/' + uploaded_file.filename
			# with open(pdfPath, 'wb') as file:
			# 	file.write(uploaded_file.read())
			
			# essayText = pdfToText(pdfPath)
			# <---> Logic for accepting pdf input and converting it into text, that is, essayText would hold a String

		essayText = "Technology has become an integral part of our lives, transforming the way we live, work, and communicate. From smartphones and laptops to smart homes and self-driving cars, technology has made our lives more convenient and efficient. It has also opened up new opportunities for innovation, creativity, and economic growth. However, as with any powerful tool, technology also presents challenges, such as privacy concerns, cybersecurity threats, and the potential for job displacement. As we continue to navigate this rapidly evolving landscape, it is important to approach technology with a critical and informed perspective, considering both its benefits and its potential risks."
		response = textModel.generate_content("Given is an essay written by a student, analyze it and give constructive feedback and score out it out of 10 marks. The topic is: " + "Technology" + essayText)
		with open(r'./analysisText/output.txt', 'w+') as fp:
			fp.write(response.text)
		return 'Done!'
	



if __name__ == '__main__':
	app.run(debug=True)