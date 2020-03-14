import sys
import numpy as np
from flask import Flask, request, render_template
import qa.question_answering as qans
#from qa.create_model import update_config
# Default url is http://localhost:5000



app = Flask(__name__)

# If docker, use 0.0.0.0
host = ('0.0.0.0' if len(sys.argv) > 1 else '127.0.0.1')


# Load in data, model

data = qans.load_data()
model = qans.load_model(data)


@app.route('/')
def home():
    """
    Description: Render default page without text
    Output: Rendered page
    """

    return render_template('index.html')


@app.route('/answer', methods = ['POST'])
def answer():
    """
    Description: Render page with answer text
    Output: Rendered page
    """

    query =  [str(x) for x in request.form.values()][0]

    ans = qans.answer_question_quick(query, model, data)


    Question = "Question: {}".format(query)
    Answer = "Answer: {}".format(str(ans[0]))
    Matching_Score = "Matching Score: {}".format(str(ans[1]))


    return render_template('index.html', question=Question, prediction=Answer, matching_score=Matching_Score)


if __name__ == "__main__":
    app.run(debug = True, host=host)