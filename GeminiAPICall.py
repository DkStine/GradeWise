# Imports
import google.generativeai as genai
import pathlib
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()

# from IPython.display import display
# from IPython.display import Markdown

# To convert output into markdown
# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# API_KEY config
GOOGLE_API_KEY = os.getenv("API_KEY")
genai.configure(api_key = GOOGLE_API_KEY)

# Model selection
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)

model = genai.GenerativeModel('gemini-pro')

# Use
response = model.generate_content("I am going to a hackathon give me some problem statements")
# print(type(response.text)) --> String
with open(r'./analysisText/output.txt', 'w+') as fp:
    fp.write(response.text)

# print(response.text)