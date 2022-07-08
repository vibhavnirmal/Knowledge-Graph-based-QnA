import json
import re

import inflect
# import pandas as pd
import spacy

from kwQnA._complex import ComplexFunc
from kwQnA._getentitypair import GetEntity


class QuestionAnswer:
    """docstring for QuestionAnswer."""

    def __init__(self):
        super(QuestionAnswer, self).__init__()
        self.complex = ComplexFunc()
        self.nlp = spacy.load('en_core_web_sm')
        self.p = inflect.engine()

    def findanswer(self, question, c):
        p = self.complex.question_pairs(question)

        if p == [] or p is None:
            return "Not Applicable"

        pair = p[0]
        # print(pair[5])

        f = open("extra/database.json","r", encoding="utf8")
        listData = f.readlines()

        relQ = []
        loaded = json.loads(listData[0])
        relationQ = self.nlp(pair[1])


        for i in relationQ:
            relationQ = i.lemma_
            relQ.append(relationQ)

        objectQ = pair[3]
        subList = []
        timeQ = str(pair[4]).lower()
        placeQ = str(pair[5]).lower()
        # print(timeQ, placeQ)

        relationQ = " ".join(relQ)
        # print(relationQ)

        if pair[0] in ('who'):

            for i in loaded:
                relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                relationSSS = " ".join([relation.lemma_ for relation in self.nlp(loaded[str(i)]["relation"])])

                relationS = [i.lemma_ for i in relationS]
                relationS = relationS[0]
                # print(relationSSS)

                if relationS == relationQ:
                    objectS = loaded[str(i)]["target"]
                    objectS = re.sub('-', ' ', objectS)
                    objectQ = re.sub('-', ' ', objectQ)
                    # print(objectQ, objectS)

                    if self.p.singular_noun(objectS):
                        objectS = self.p.singular_noun(objectS)
                    if self.p.singular_noun(objectQ):
                        objectQ = self.p.singular_noun(objectQ)

                    if objectS == objectQ:
                        if str(pair[4]) != "":
                            timeS = [str(loaded[str(i)]["time"]).lower()]
                            # print(timeQ, timeS)
                            if timeQ in timeS:
                                answer_subj = loaded[str(i)]["source"]
                                subList.append(answer_subj)
                        else:
                            answer_subj = loaded[str(i)]["source"]
                            subList.append(answer_subj)
                elif str(relationSSS) == str(relationQ):
                    objectS = loaded[str(i)]["target"]
                    objectS = re.sub('-', ' ', objectS)

                    if objectS == objectQ:
                        if str(pair[4]) != "":
                            timeS = [str(loaded[str(i)]["time"]).lower()]
                            if timeQ in timeS:
                                answer_subj = loaded[str(i)]["source"]
                                subList.append(answer_subj)
                        else:
                            answer_subj = loaded[str(i)]["source"]
                            subList.append(answer_subj)


            answer_subj = ",".join(subList)
            if answer_subj == "":
                return "None"
            return answer_subj

        elif pair[3] in ['what']:
            subjectQ = pair[0]
            subList = []
            for i in loaded:
                subjectS = loaded[str(i)]["source"]
                # print(subjectQ, subjectS)
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    if len(relationS) > 1:
                        relationS = " ".join(relationS)
                    else:
                        relationS = relationS[0]
                    # print(relationQ, relationS)
                    if relationQ == relationS:
                        if str(pair[5]) != "":
                            placeS = [str(place).lower() for place in self.nlp(loaded[str(i)]["place"])]
                            # print(placeQ, placeS)
                            if placeQ in placeS:
                                if str(pair[4]) != "":
                                    timeS = [str(time).lower() for time in self.nlp(loaded[str(i)]["time"])]
                                    if timeQ in timeS:
                                        answer_subj = loaded[str(i)]["target"]
                                        subList.append(answer_subj)
                                else:
                                    answer_subj = loaded[str(i)]["target"]
                                    subList.append(answer_subj)
                        else:
                            if str(pair[4]) != "":
                                timeS = [str(time).lower() for time in self.nlp(loaded[str(i)]["time"])]
                                if timeQ in timeS:
                                    answer_subj = loaded[str(i)]["target"]
                                    subList.append(answer_subj)
                            else:
                                answer_subj = loaded[str(i)]["target"]
                                subList.append(answer_subj)

            answer_obj = ",".join(subList)
            if answer_obj == "":
                return "None"
            return answer_obj

        elif pair[4] in ['when']:
            subjectQ = pair[0]
            # print(relationQ, subjectQ)
            # print(pair[2])
            for i in loaded:
                # if i.dep_ in ('obj'):
                # print(loaded[str(i)], "HERE we go")
                subjectS = loaded[str(i)]["source"]
                # print(type(subjectQ), type(subjectS), numberOfPairs)
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    # print(relationS)
                    relationS = [i.lemma_ for i in relationS]
                    relBuffer = relationS
                    # print(relationS[0], relationS[1])
                    # print(relBuffer[1])

                    if len(relBuffer) < 2:
                        relationS = relBuffer[0]
                    else:
                        if str(relBuffer[1]).lower() == 'to':
                            relationS = " ".join(relationS)
                        else:
                            relationS = relationS[0]
                            extraIN = relBuffer[1].lower()

                    # print(relationQ, relationS)
                    if relationQ == relationS:
                        if str(pair[5]) != "":
                            placeS = [str(place).lower() for place in self.nlp(loaded[str(i)]["place"])]
                            # print(placeQ, placeS)
                            if placeQ in placeS:
                                if loaded[str(i)]["time"] != '':
                                    answer_obj = loaded[str(i)]["time"]
                                # elif extraIN == "in" or extraIN == "on":
                                    # answer_obj = loaded[str(i)]["target"]
                                    return answer_obj
                                return None
                        else:
                            if loaded[str(i)]["time"] != '':
                                answer_obj = loaded[str(i)]["time"]
                                return answer_obj
                            return None

        elif pair[5] in ['where']:
            subjectQ = pair[0]
            for i in loaded:
                subjectS = loaded[str(i)]["source"]
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relationS = relationS[0]

                    if relationQ == relationS:
                        if str(pair[4]) != "":
                            timeS = [str(time).lower() for time in self.nlp(loaded[str(i)]["time"])]
                            if timeQ in timeS:
                                answer_obj = loaded[str(i)]["place"]
                                if answer_obj in (" ",""):
                                    if int(i)<int(len(loaded)-1):
                                        pass
                                    return None
                                return answer_obj
                            return None
                        
                        answer_obj = loaded[str(i)]["place"]
                        if answer_obj in (" ",""):
                            if int(i)<int(len(loaded)-1):
                                pass
                            return None
                        return answer_obj
