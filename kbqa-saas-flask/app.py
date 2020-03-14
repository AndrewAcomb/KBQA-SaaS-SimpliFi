from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from flask_pusher import Pusher
from werkzeug.utils import secure_filename
from contextlib import redirect_stdout
from time import sleep

import subprocess
import os
import sys  

sys.path.append('/Users/andrewacomb/Desktop/School/Current_Classes/COMP_SCI_496/repo/kbqa-saas-flask/question-answering')  
from question_answering import answer_question

app_id = "960906"
key = "d18ed2e42cf337876806"
secret = "ffd3ef254ef8617ab31a"
cluster = "us2"

app = Flask(__name__)
pusher = Pusher(app, secret = secret, app_id = app_id, key = key, cluster = cluster)


app.secret_key = 'secret key'
CORS(app)

UPLOAD_FOLDER = './data_upload'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def write_to_pusher(message):
    
    if isinstance(message, bytes):
        message = message.decode('utf-8')
    
    messages = message.split('\n')
    for message in messages:
        sleep(.3)
        pusher.trigger('pipeline', 'progress', {'message': message})

def build_data(data_file_path):
    
    messages = subprocess.check_output(['python3', './data-parsing/data_util.py', data_file_path])
    write_to_pusher(messages)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def train_model():

    for message in execute(['python3', './question-answering/run_all.py', 'update_config']):
        print(message)
        write_to_pusher(message)

    for message in execute(['python3', './question-answering/run_all.py', 'generate_embeddings']):
        print(message)
        write_to_pusher(message)

    for message in execute(['python3', './question-answering/run_all.py', 'build_training_data']):
        print(message)
        write_to_pusher(message)

    for message in execute(['python3', './question-answering/run_all.py', 'train_model']):
        print(message)
        write_to_pusher(message)

def save_raw_data(file):

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    write_to_pusher("{} saved".format(filename))

    return file_path

@app.route('/upload', methods=['POST'])
def upload_file():
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file in request')
        return 'No file in request'

    file = request.files['file']
 
    if file and allowed_file(file.filename):

        file_path = save_raw_data(file)
        build_data(file_path)
        train_model()

        write_to_pusher("API endpoint: http://127.0.0.1:5000/answer")

        print('File uploaded')
        return 'File uploaded'

    print('Reach end error')
    return 'Reach end error'
    
@app.route('/answer', methods=['GET'])
def query():
    #Ex: http://127.0.0.1:5000/answer?question=what_is_the_revenue_of_$aapl_?
    question = request.args.get('question').replace("_", " ")

    return answer_question(question)





