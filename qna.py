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
        relQ = []
        relationQ = self.nlp(pair[1])
        for i in relationQ:
            relationQ = i.lemma_
            relQ.append(relationQ)

        relationQ = " ".join(relQ)
        # print(relationQ)
        # print(relQ)

        if pair[0] in ('who'):
            objectQ = pair[2]
            subList = []
            # print(objectQ)

            for i in loaded:
                relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                relationSSS = " ".join([relation.lemma_ for relation in self.nlp(loaded[str(i)]["relation"])])
                # print(relationSSS)
                relationS = [i.lemma_ for i in relationS]
                relationS = relationS[0]
                # print(relationS, relationQ)
                # print(objectQ, loaded[str(i)]["target"])
                if relationS == relationQ:
                    # print(loaded[str(i)]["target"])
                    if loaded[str(i)]["target"] == objectQ:
                        answer_subj = loaded[str(i)]["source"]
                        # print(answer_subj, "hoilll")
                        subList.append(answer_subj)
                        # print(answer_subj)
                elif str(relationSSS) == str(relationQ):
                    # print(loaded[str(i)]["target"])
                    if loaded[str(i)]["target"] == objectQ:
                        answer_subj = loaded[str(i)]["source"]
                        # print(answer_subj, "hoilll")
                        subList.append(answer_subj)
                        # print(answer_subj)

            answer_subj = ",".join(subList)
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

        elif pair[2] in ('where'):
            subjectQ = pair[0]
            # print(relationQ, subjectQ)
            # print(pair[2])
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

        elif pair[5] in ('when'):
            subjectQ = pair[0]
            # print(subjectQ)
            # print(relationQ, subjectQ)
            # print(pair[2])
            for i in loaded:
                # if i.dep_ in ('obj'):
                # print(loaded[str(i)], "HERE we go")
                subjectS = loaded[str(i)]["source"]
                # print(type(subjectQ), type(subjectS), numberOfPairs)
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relationS = " ".join(relationS)
                    # print(relationQ)
                    # print(relationS)

                    if relationQ == relationS:
                        answer_obj = loaded[str(i)]["date"]
                        return answer_obj
