# Imports
import google.generativeai as genai
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
app.config['MONGO_URI'] = 'mongodb://localhost:27017/model'
mongo = PyMongo(app)

# Gemini_API_KEY config
GOOGLE_API_KEY = os.getenv("API_KEY")
genai.configure(api_key = GOOGLE_API_KEY)

# Gemini model selection
model = genai.GenerativeModel('gemini-pro')

# --> PDF2Image
poppler_path = r"C:/Users/91993/Downloads/Programs/Release-24.02.0-0/poppler-24.02.0/Library/bin"

#path of pdf 
pdf_path = r"./essayPdf/Course Plan Eng Phy.pdf"


pages =convert_from_path(pdf_path = pdf_path, poppler_path = poppler_path)
import os 
#path to savdthe output in.
saving_folder = r"./essayImages/"

#to countthe number of pages
counter = 1
#iterateover all the pages of the pdf
for page in pages:
    img_name = f"Page_0{counter}.png"
    page.save(os.path.join(saving_folder,img_name), "PNG")
    counter += 1

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

# GET method logic
@app.route('/handle_get', methods=['GET'])
def handle_get():
	if request.method == 'GET':
		username = request.args['username']
		password = request.args['password']
		print(username, password)
		if username in users and users[username] == password:
			return '<h1>Welcome!!!</h1>'
		else:
			return '<h1>invalid credentials!</h1>'
	else:
		return render_template('login.html')

# POST method logic
@app.route('/handle_post', methods=['POST'])
def handle_post():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		print(username, password)
		if username in users and users[username] == password:
			return '<h1>Welcome!!!</h1>'
		else:
			return '<h1>invalid credentials!</h1>'
	else:
		return render_template('login.html')

@app.route('/handle_upload', methods = ['POST'])
def handle_upload():
	if 'pdfFile' in request.files:
	# 	pdfFile = request.files['pdfFile']
	# 	mongo.save_file(pdfFile.filename, pdfFile)
	# 	mongo.db.assignment.insert_one({'username' : request.form.get('username'), 'pdfFileName' : pdfFile.filename})
		uploaded_file = request.files['pdfFile']
		if uploaded_file.filename != '':
			uploaded_file.save('./essayPdf/', uploaded_file.filename)


	essayText = "Technology has become an integral part of our lives, transforming the way we live, work, and communicate. From smartphones and laptops to smart homes and self-driving cars, technology has made our lives more convenient and efficient. It has also opened up new opportunities for innovation, creativity, and economic growth. However, as with any powerful tool, technology also presents challenges, such as privacy concerns, cybersecurity threats, and the potential for job displacement. As we continue to navigate this rapidly evolving landscape, it is important to approach technology with a critical and informed perspective, considering both its benefits and its potential risks."
	response = model.generate_content("Given is an essay written by a student, analyze it and give constructive feedback and score out it out of 10 marks. The topic is: " + "Technology" + essayText)
	with open(r'./analysisText/output.txt', 'w+') as fp:
		fp.write(response.text)
	return 'Done!'


if __name__ == '__main__':
	app.run(debug=True)
