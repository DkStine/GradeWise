# Imports
import google.generativeai as genai
from PIL import Image
import pytesseract
import pathlib
import textwrap
import os
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
model = genai.GenerativeModel('gemini-pro')

# # --> PDF2Image
# poppler_path = r"C:/Users/91993/Downloads/Programs/Release-24.02.0-0/poppler-24.02.0/Library/bin"

# #path of pdf 
# pdf_path = r"./essayPdf/Course Plan Eng Phy.pdf"


# pages =convert_from_path(pdf_path = pdf_path, poppler_path = poppler_path)
# #path to savdthe output in.
# saving_folder = r"./essayImages/"

# #to count the number of pages
# counter = 1
# #iterateover all the pages of the pdf
# for page in pages:
#     img_name = f"Page_0{counter}.png"
#     page.save(os.path.join(saving_folder,img_name), "PNG")
#     counter += 1

def pdfToText(pdfPath):
		with Image.open(pdfPath) as img:
			width, height = img.size
			for i in range(height // width + 1):
				page = img.crop((0, i * width, width, i * width))
				page.save('./essayImages/{}.png'.format(i))

		text = ""

# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'

# dictionary to store user and password
users = {
	'kunal': '1234',
	'user2': 'password2'
}

essayText = ""

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
			uploaded_file = request.files['pdfFile']
			pdf_path = '/tmp/' + uploaded_file.filename
			with open(pdf_path, 'wb') as file:
				file.write(uploaded_file.read())
			
			essayText = pdfToText(pdf_path)


	# essayText = "Technology has become an integral part of our lives, transforming the way we live, work, and communicate. From smartphones and laptops to smart homes and self-driving cars, technology has made our lives more convenient and efficient. It has also opened up new opportunities for innovation, creativity, and economic growth. However, as with any powerful tool, technology also presents challenges, such as privacy concerns, cybersecurity threats, and the potential for job displacement. As we continue to navigate this rapidly evolving landscape, it is important to approach technology with a critical and informed perspective, considering both its benefits and its potential risks."
	# response = model.generate_content("Given is an essay written by a student, analyze it and give constructive feedback and score out it out of 10 marks. The topic is: " + "Technology" + essayText)
	# with open(r'./analysisText/output.txt', 'w+') as fp:
	# 	fp.write(response.text)
	# return 'Done!'


if __name__ == '__main__':
	app.run(debug=True)
