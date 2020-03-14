import re
import spacy
import neuralcoref
import pandas as pd
from complex import Complexx
from prepro import Prepro
from util import Utility


class mainFunc:
    """docstring for main."""

    def __init__(self):
        super(mainFunc, self).__init__()
        self.complex = Complexx()
        self.prepro = Prepro()
        self.util = Utility()
        self.sentence_of_mine = ""
        self.nlp = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(self.nlp)

    def check_for_and_(self, sentence):
        x = []
        count = 0
        for word in sentence:
            count += 1
            if word.dep_ in ('cc'):
                p1 = count-1
                x.append(p1)
        # print(x)

        depen = []
        for i in x:
            depen.append([word.dep_ for word in sentence[:i]])

        # print(depen)
        newcount = -1
        senten1, senten2 = "", ""
        # , ["subj", "ROOT", "dobj"], ["subj", "ROOT", "pobj"], ["nsubj", "ROOT", "obj"], ["nsubj", "ROOT", "dobj"], ["nsubj", "ROOT", "pobj"], ["nsubjpass", "ROOT", "obj"], ["nsubjpass", "ROOT", "dobj"], ["nsubjpass", "ROOT", "pobj"]]
        list2 = ["nsubj", "ROOT", "dobj"]

        for i in depen:
            newcount += 1
            list1 = i
            check = all(item in list1 for item in list2)
            # print(check)

            if check:
                return True
            else:
                pass


    def diff_sent_return(self, sentence):

        x = []
        count = 0
        for word in sentence:
            count += 1
            if word.dep_ in ('cc'):
                p1 = count-1
                x.append(p1)
        # print(x)

        depen = []
        for i in x:
            depen.append([word.dep_ for word in sentence[:i]])

        # print(depen)
        newcount = -1
        senten1, senten2 = "", ""
        # , ["subj", "ROOT", "dobj"], ["subj", "ROOT", "pobj"], ["nsubj", "ROOT", "obj"], ["nsubj", "ROOT", "dobj"], ["nsubj", "ROOT", "pobj"], ["nsubjpass", "ROOT", "obj"], ["nsubjpass", "ROOT", "dobj"], ["nsubjpass", "ROOT", "pobj"]]
        list2 = ["nsubj", "ROOT", "dobj"]

        for i in depen:
            newcount += 1
            list1 = i
            check = all(item in list1 for item in list2)
            if check:
                lista = [str(w) for w in sentence]

                p1 = lista[:x[newcount]]
                p2 = lista[x[newcount]+1:]

                senten1 = " ".join(p1)
                senten2 = " ".join(p2)

                senten1 = self.nlp(senten1)
                senten2 = self.nlp(senten2)

                # print(senten1)
                # print(senten2)
                # break

        return str(senten1), str(senten2)

    def get_entity(self, filename, coref = True):
        with open(filename,"r+") as new:
            for text in new:
                # print(text)
                text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
                text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
                text = self.nlp(text)

            if coref:
                text = self.nlp(text._.coref_resolved)  # resolve coreference clusters

        # text = self.nlp("I saw a man you love")
        # print(self.nlp(text._.coref_resolved))

        sentences = [sent.string.strip() for sent in text.sents]  # split text into sentences
        print(sentences)
        count3 = 0

        for sent in sentences:
            sent = self.nlp(sent)
            checked_for_and = self.check_for_and_(sent)
            print(checked_for_and)

            if checked_for_and:
                sent1, sent2 = self.diff_sent_return(sent)
                # print(sent1, sent2)
                text = str(sent1) + ". " +str(sent2)
                text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
                text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
                text = self.nlp(text)
                sent = self.nlp(text._.coref_resolved)

                mko = sent

                sentgg = str(mko).split(".")

                for i in sentgg:
                    count3 = count3 + 1
                    newio = self.nlp(i)

                    print(newio)
                    dep = [token.dep_ for token in newio]
                    # print(dep)

                    ent_pairs , object_che = self.util.which_sent(dep, newio)
                    # print(ent_pairs)

                    self.final_ent_pairs(ent_pairs, object_che)

            else:
                spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
                spans = spacy.util.filter_spans(spans)
                print(spans)
                with sent.retokenize() as retokenizer:
                    [retokenizer.merge(span) for span in spans]

                dep = [token.dep_ for token in sent]
                print(dep)

                ent_pairs , object_che = self.util.which_sent(dep, sent)
                print(ent_pairs)

                self.final_ent_pairs(ent_pairs, object_che)


    def final_ent_pairs(self, ent_pairs, object_che):
        filtered_entpairs = [sublist for sublist in ent_pairs if not any(str(x) == '' for x in sublist)]

        if object_che == False:
            pairs = pd.DataFrame(filtered_entpairs, columns=['subject', 'relation', 'subject_type'])
        elif object_che == True:
            pairs = pd.DataFrame(filtered_entpairs, columns=['subject', 'relation', 'object', 'subject_type', 'object_type'])
        else:
            pass

        print('Entity pairs extracted:', str(len(filtered_entpairs)))
        print(pairs)
