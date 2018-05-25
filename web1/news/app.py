import json
from flask import Flask,render_template,redirect,abort
import os
import re

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

def get_json():
	result={}
	file_list=os.listdir('/home/shiyanlou/files/')
	for file in file_list:
		with open(os.path.join('/home/shiyanlou/files/',file)) as f:
			result[file.split('.')[0]]=json.loads(f.read())
	return result

files=get_json()
for value in files.values():
	re.sub(r'\*n','',value['content'])

@app.route('/')
def index():
	titles=[]
	for value in files.values():
		titles.append(value['title'])
	return render_template('index.html',titles = titles)

@app.route('/files/<filename>')
def file(filename):
	if filename not in files.keys():
		abort(404)
	return render_template('file.html', filename=files[filename])

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404

if __name__ == "__main__":
	# app.run()
	print(files)