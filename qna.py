from getentitypair import GetEntity
import spacy
import pandas as pd
from complex import Complexx
import json

class QuestionAnswer:
    """docstring for QuestionAnswer."""

    def __init__(self):
        super(QuestionAnswer, self).__init__()
        self.complex = Complexx()
        self.nlp = spacy.load('en_core_web_sm')
        # neuralcoref.add_to_pipe(self.nlp)

    def findanswer(self, question, numberOfPairs):
        # print(question)
        p = self.complex.question_pairs(question)
        # print(p)
        pair = p[0]
        # print(pair)

        f = open("database.json","r", encoding="utf8")
        listData = f.readlines()

        loaded = json.loads(listData[0])
        # print(loaded)

        relationQ = self.nlp(pair[1])
        for i in relationQ:
            relationQ = i.lemma_

        if pair[0] in ('who'):
             objectQ = pair[2]

             for i in loaded:
                 relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                 relationS = [i.lemma_ for i in relationS]
                 relationS = relationS[0]
                 # print(relationS)

                 if relationS == relationQ:
                     # print(objectQ)
                     if loaded[str(i)]["target"] == objectQ:
                         answer_subj = loaded[str(i)]["source"]
                         return answer_subj

        elif pair[2] in ('what'):
            subjectQ = pair[0]
            # print(relationQ, subjectQ)

            for i in loaded:
                subjectS = loaded[str(i)]["source"]
                # print(subjectQ, subjectS, numberOfPairs)
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relationS = relationS[0]
                    # print(relationS)

                    if relationQ == relationS:
                        answer_obj = loaded[str(i)]["target"]
                        return answer_obj
