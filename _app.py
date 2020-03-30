from flask import Flask, render_template, url_for, request, jsonify
from _getentitypair import GetEntity
from _qna import QuestionAnswer
from _exportPairs import exportToJSON
import json
from datetime import datetime

app = Flask(__name__)


# p = open("database.json", "r")
#
# __data = json.load(p)
#
# print(__data)


def getAnswer(paragraph, question):
    getent = GetEntity()
    qa = QuestionAnswer()
    export = exportToJSON()
    refined_text = getent.preprocess_text([paragraph])
    # print(refined_text)
    dataEntities, numberOfPairs = getent.get_entity(refined_text)
    export.dumpdata(dataEntities[0])
    # print(dataEntities)
    outputAnswer = qa.findanswer(str(question), numberOfPairs)
    return outputAnswer


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route('/select', methods=['GET', 'POST'])
def select():
    return jsonify(result={"titles" : titles, "contextss" : contextss, "context_questions" : context_questions})

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    paragraph = str(request.form["paragraph"])
    question = str(request.form["question"])
    # return jsonify(result=answer)
    my_answer = getAnswer(paragraph, question)
    return render_template('index.html', my_answer=my_answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=20550, threaded=True)
