# import networkx as nx
# import matplotlib.pyplot as plt
from getentitypair import GetEntity
# from exportPairs import exportToJSON
import pandas as pd
# from complex import Complexx
import json

class QuestionAnswer:
    """docstring for QuestionAnswer."""

    def __init__(self):
        super(QuestionAnswer, self).__init__()
        self.complex = Complexx()
        # self.x = GetEntity()

    def findanswer(self, question):
        p = self.complex.question_pairs(question)
        pair = p[0]
        if pair[0] in ('Who','who','wHo', 'WHO', 'whO','WHo'):
             relation = pair[1]
             object = pair[2]

             f = open("database.json","r", encoding="utf8")

             listData = f.readlines()
             mahData = listData[0]

             loaded = json.loads(mahData)
             print(loaded)


             print(loaded["0"])


        elif p[0][0] in ('What'):
            print("IN WHAT")
