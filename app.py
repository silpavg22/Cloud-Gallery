from flask import Flask, flash,request, render_template, redirect
from werkzeug.utils import secure_filename
import os
import csv
from tempfile import NamedTemporaryFile
import shutil
import os.path
from os import path

app = Flask(__name__, static_folder='static', static_url_path='')

app.config.from_pyfile('config.py')
account = app.config['ACCOUNT_NAME']  # Azure account name
key = app.config['ACCOUNT_KEY']  # Azure Storage account access key
connect_str = app.config['CONNECTION_STRING']
container = app.config['CONTAINER']  # Container name
allowed_ext = app.config['ALLOWED_EXTENSIONS']  # List of accepted extensions
max_length = app.config['MAX_CONTENT_LENGTH']  # Maximum size of the uploaded file
sas_url = app.config['BLOB_SAS_URL']  # Maximum size of the uploaded file
upload_folder=app.config['UPLOAD_FOLDER']

# below variables are used in multiple fns
people_dict = {}
file_name = "static/people.csv"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_ext


@app.route("/")
def home():
    people = read_people_file()
    if(path.exists(file_name)):
        return render_template('index.html', people_dict=people)
    else:
        return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    msg=''
    people = read_people_file()
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        msg = "Please select a file!!"
        return render_template('index.html',people_dict=people,msg=msg)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        msg='File successfully uploaded'
        name_to_upload = request.form.get('name_to_upload')
        update_person_pic(name_to_upload,filename)
        people = read_people_file()
        return render_template('index.html',people_dict=people, filename=filename,msg=msg)



@app.route('/searchpeople', methods=['GET'])
def getPerson():
    people = read_people_file()
    name_to_search = request.args.get('search_people')
    print(name_to_search)
    person_data = people[name_to_search]
    return render_template("index.html", person_data=person_data, people_dict=people)


@app.route('/findpeoplewithsalary', methods=['GET'])
def findpeoplewithsalary():
    peoples = read_people_file()
    arr = []
    salary_to_search = request.args.get('findpeoplewithsalary')
    print(salary_to_search)
    for key, value in peoples.items():
        current_salary = int(value['Salary'].strip() or 0)
        if current_salary > int(salary_to_search):
            arr.append(value)
    print(arr)
    return render_template("index.html", people_dict=peoples, peoplearr=arr)


def read_people_file():

    if(path.exists(file_name)):
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                people_dict[row['Name'].lower()] = row
        return people_dict

#https://stackoverflow.com/questions/46126082/how-to-update-rows-in-a-csv-file
def update_person_pic(name,image_name):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['Name', 'State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
    with open(file_name, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Name'].lower() == name:
                row['Picture'] = image_name
            writer.writerow(row)
    shutil.move(tempfile.name, file_name)


@app.route('/updatekey', methods=['GET'])
def update_keyword():
    name = request.args.get('nametoupdate')
    keyword = request.args.get('updatekey')
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['Name', 'State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
    with open(file_name, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Name'].lower() == name:
                row['Keywords'] = keyword
            writer.writerow(row)
    shutil.move(tempfile.name, file_name)
    peoples = read_people_file()
    return render_template("index.html", people_dict=peoples)


@app.route('/updatesalary', methods=['GET'])
def update_salary():
    name = request.args.get('nameupdated')
    salary = request.args.get('updatesalary')
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['Name', 'State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
    with open(file_name, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Name'].lower() == name:
                row['Salary'] = salary
            writer.writerow(row)
    shutil.move(tempfile.name, file_name)
    peoples = read_people_file()
    return render_template("index.html", people_dict=peoples)


@app.route('/deleteentry', methods=['GET'])
def deleteentry():
    name = request.args.get('nametodelete')
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['Name', 'State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
    with open(file_name, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Name'].lower() != name:
               writer.writerow(row)
    shutil.move(tempfile.name, file_name)
    peoples = read_people_file()
    return render_template("index.html", people_dict=peoples)


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
