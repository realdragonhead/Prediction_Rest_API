import numpy as np
import urllib.request
import cv2
import os
import sys
import csv
sys.path.append('/Users/dragonheadreal/Documents/dragonnest/project/restAPI/callrestAPI/robo_jejunu_face_feature_extract/')
import faces_feature_extract
from flask import Flask, session, render_template, request
from werkzeug import secure_filename

# -*- coding:utf-8 -*-
###############################################
#--------------- Flask restAPI ---------------#
#------------------------ made by dragonhead -#
###############################################

app = Flask (__name__)

# Set path and file's name where image will be saved
# Input base directory that temporary image will be saved
target = "/Users/dragonheadreal/Documents/dragonnest/project/restAPI/callrestAPI/robo_jejunu_face_feature_extract/target.jpg"


# All Function list used by API
def predictFace(path):
	result = faces_feature_extract.full_feature_extraction(path)
	print(result)
	return result
def url_to_image(url):
	path = urllib.request.urlretrieve(url, target)

# Rendering index.html and shown to browser
# Root API
@app.route('/')
def index_page_loader():
	return render_template('index.html')

# Working test
# For test restAPI server working now(status)
@app.route('/test')
def test_working():
	return render_template('test.html')

# send, reply test
# For test restAPI server working in GET method(send, reply)
@app.route('/testsend', methods=['POST'])
def test_send():
	got_test_word = request.form['send_test_word']
	return '"%s" is string that user send me'%(got_test_word)

# get file from form by 'POST' method
@app.route('/fileuploader', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return "Complete save to server's root directory"	

# For making image from url image
@app.route('/makeimage', methods=['POST'])
def url_to_image_func():
	temp_url = request.form['url']
	path = urllib.request.urlretrieve(temp_url, target)
	return 'Done making image!'

# Do predict immediately
@app.route('/fileupload_and_predict', methods=['GET', 'POST'])
def image_upload_predict():
	if request.method == 'POST':
		f = request.files['file']
		fname = f.filename
		f.save(secure_filename(fname))
		result = predictFace(fname)
		return '%s'%(result)

# Predict age and gender by detect function
@app.route('/predict')
def predict_face():
	result = predictFace(target)
	return 'Saving Face info to CSV is done : %s'%(result)

# All routine save image from url, predict and saved result to CSV file
@app.route('/routine', methods=['GET', 'POST'])
def all_routine():
	if request.method == 'POST':
		f = request.files['file']
		fname = f.filename
		f.save(secure_filename(fname))
		
		fd_index = open('index.csv', 'r', encoding='utf-8')
		fd_index_err = open('index.csv', 'r', encoding='euc-kr')
		fd_kr = open(fname, 'r', encoding='euc-kr')
		fd = open(fname, 'r', encoding='utf-8')

		rdr_index = csv.reader(fd_index)
		rdr_index_err = csv.reader(fd_index_err)
		rdr_kr = csv.reader(fd_kr)
		rdr = csv.reader(fd)
		
		try :
			for line_index in rdr_index:
				temp_url_index = line_index[1]
		except :
			for line_index_err in rdr_index_err:
				temp_url_index = line_index_err[1]
		
		url_index = int(temp_url_index)
		try :
			for line_kr in rdr_kr:
				print(line_kr[url_index])
				if line_kr[url_index] == ' ':
					continue
				url_to_image(line_kr[url_index])	
				predictFace(target)
		except :
			for line in rdr:
				print(line[url_index])
				if line[url_index] == ' ':
					continue
				url_to_image(line[url_index])
				predictFace(target)
			
		fd_index.close()
		fd_index_err.close()
		fd_kr.close()
		fd.close()
		return 'done'

# Search on database with index
# Help to get user want info from databases
# (x-y) means get all values from x column to y column
# (a.b) means get all values from a column b row's value
# formation : x-y@a.b
# all index start from 0
# all value => 0-0@0.0
# Only third column and third value => 0-3@0.3
# from column 1 to 5 all values => 1-5@0.0
# from column 1 to 5 third values => 1-5@0.3
# from column 1 to 5, from row 1 to 3 => 1-5@1.3

@app.route('/searchindex/<formation>')
def read_csv():
	f = open('target.csv', 'r', encoding='euc-kr')
	rdr = csv.reader(f)
	
	if(formtion.find('@')):
		middle = formation.find('@')
		front = formation[:middle - 1]
		rear = formation[middle + 1:]
		
		if(front.find('-')):
			middle = front.find('-')
			col_F = front[:middle - 1]
			col_R = front[middle + 1:]
			col_S = int(col_F) - 1
			col_E = int(col_R) - 1

			if(rear. find('.')):
				middle = rear.find('.')
				row_F = front[:middle - 1]
				row_R = front[middle + 1:]
				row_S = int(row_F) - 1
				row_E = int(row_R) - 1
			
				if col_S == -1 and col_E == -1:
					col_S = 0
					col_E = len(rdr)
				if col_S == -1 and col_E != -1:
					col_S = col_E
				if row_S == -1 and row_E == -1:
					row_S = 0
					row_E = 6
				if row_S == -1 and row_E != -1:
					row_S = row_E

				
				for line in rdr:
					if col_S <= i and i<col_E:
						# Read index result process
						print(line[row_S][row_E])
				
				return 'Done'

	print('Please input right formation')


# Run API
if __name__ == "__main__":
	app.run()
