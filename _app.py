# import json
from datetime import datetime

# import pandas
from flask import Flask, jsonify, redirect, render_template, request, url_for

from kwQnA._exportPairs import exportToJSON
from kwQnA._getentitypair import GetEntity
from kwQnA._qna import QuestionAnswer

app = Flask(__name__)


class CheckAndSave:
    """docstring for CheckAndSave."""

    def __init__(self):
        super(CheckAndSave, self).__init__()

    def createdataset(self, para, que, ent, ans1, ans2):

        wholedata = {"para":[str(para)],"que":[[str(que)]], "entities":[ent], "ans1": [ans1], "ans2":[ans2]}
        # print(wholedata)
        # return None

class OurModel:
    def __init__(self):
        self.getent = GetEntity()
        self.qa = QuestionAnswer()
        self.export = exportToJSON()

    def getAnswer(self, paragraph, question):

        refined_text = self.getent.preprocess_text([paragraph])
        dataEntities, numberOfPairs = self.getent.get_entity(refined_text)

        if dataEntities:
            # data_in_dict = dataEntities[0].to_dict()
            self.export.dumpdata(dataEntities[0])
            outputAnswer = self.qa.findanswer(str(question), numberOfPairs)
            if outputAnswer == []:
                return None
            return outputAnswer
        return None


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    return redirect(url_for('main'))

# @app.route('/select', methods=['GET', 'POST'])
# def select():
#     return jsonify(result={"titles" : titles, "contextss" : contextss, "context_questions" : context_questions})

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # model1 = MachineComprehend()
    model2 = OurModel()
    save = CheckAndSave()
    # if request.form["clear"] == 'clear':
    #     return redirect('/')
    input_paragraph = str(request.form["paragraph"])
    input_question = str(request.form["question"])
    # bidaf_answer = model1.answer_question(input_paragraph, input_question)
    my_answer = model2.getAnswer(input_paragraph, input_question)

    # save.createdataset(input_paragraph, input_question, data_in_dict, my_answer, bidaf_answer)

    return render_template('index.html', my_answer=my_answer, input_paragraph=input_paragraph ,input_question=input_question)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=20550, threaded=True)
