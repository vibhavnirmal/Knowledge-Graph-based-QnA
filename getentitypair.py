import re
import spacy
import neuralcoref
import pandas as pd
from complex import Complexx
from prepro import Prepro
from util import Utility


class GetEntity:
    """docstring for GetEntity."""

    def __init__(self):
        super(GetEntity, self).__init__()
        self.complex = Complexx()
        self.prepro = Prepro()
        self.util = Utility()
        self.sentence_of_mine = ""
        self.nlp = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(self.nlp)

    def check_for_multi_and_(self, sentence):
        x = []
        count = 0
        for word in sentence:
            # print([i for i in word.subtree])
            count += 1
            if word.dep_ in ('cc'):
                x.append(count-1)
                # print([i for i in word.head.rights if i.dep_ in ('obj', 'dobj', 'pobj')])
                # print([i for i in word.head.rights if i.dep_ in ('nsubj', 'nsubjpass', 'subj')])
                # print([i for i in word.head.rights if i.dep_ in ('conj')])
        # print(x)

        depen = []
        for i in x:
            depen.append([word.dep_ for word in sentence[:i]])

        senten1, senten2 = "", ""
        list2 = ["nsubj", "ROOT", "dobj"]
        # , ["subj", "ROOT", "dobj"], ["subj", "ROOT", "pobj"], ["nsubj", "ROOT", "obj"], ["nsubj", "ROOT", "dobj"], ["nsubj", "ROOT", "pobj"], ["nsubjpass", "ROOT", "obj"], ["nsubjpass", "ROOT", "dobj"], ["nsubjpass", "ROOT", "pobj"]]

        for list1 in depen:
            check = all(item in list1 for item in list2)
            #
            # print(list1)

            if check:
                # print(depen, x)
                return True, depen, x
            else:
                pass

        return False, [], 0


    def diff_sent_return(self, sentence, depen, pos_of_and):
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

                p1 = lista[:pos_of_and[newcount]]
                p2 = lista[pos_of_and[newcount]+1:]

                # print(p1, p2)

                senten1 = " ".join(p1)
                senten2 = " ".join(p2)

                senten1 = self.nlp(senten1)
                senten2 = self.nlp(senten2)

        return str(senten1), str(senten2)

    def get_entity(self, filename, coref = True):
        gfgf = open(filename,"r+")
        okok = [text.strip() for text in gfgf]
        popo = [text for text in okok if text not in ('', ' ')]
        # print(popo)
        # with open(filename,"r+") as new:
        #     for text in new:
        #         # print(text)
        #         text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
        #         text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
        #         text = self.nlp(text)
        #
        #     if coref:
        #         text = self.nlp(text._.coref_resolved)  # resolve coreference clusters

        # text = self.nlp("I saw a man you love")
        # print(self.nlp(text._.coref_resolved))

        text = " ".join(popo)

        text = self.nlp(text)
        text = self.nlp(text._.coref_resolved)

        sentences = [sent.string.strip() for sent in text.sents]  # split text into sentences
        # print(sentences)
        gfinal_pair = []
        for sent in sentences:
            sent = self.nlp(sent)
            # self.going_from_root(sent, True, False, False)
            # checked_for_and , depend , pos_of_and_= self.check_for_multi_and_(sent)
            # print(checked_for_and)

            # if checked_for_and:
            #     sent1, sent2 = self.diff_sent_return(sent, depend, pos_of_and_)
            #     # print(sent1, sent2)
            #     text = str(sent1) + ". " +str(sent2)
            #     text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
            #     text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
            #     text = self.nlp(text)
            #     # sent = self.nlp(text._.coref_resolved)
            #     #
            #     # mko = sent
            #
            #     sent = str(self.nlp(text._.coref_resolved)).split(".")
            #     # print(sentgg)
            #
            #     for i in sent:
            #         new_m_sent = self.nlp(i)
            #
            #         dep = [token.dep_ for token in new_m_sent]
            #         print(dep)
            #
            #         ent_pairs , object_che = self.util.which_sent(dep, new_m_sent)
            #
            #         self.final_ent_pairs(ent_pairs, object_che)

            # else:
            spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
            spans = spacy.util.filter_spans(spans)
                # print(spans)
            with sent.retokenize() as retokenizer:
                [retokenizer.merge(span) for span in spans]

            dep = [token.dep_ for token in sent]
            pos = [token.pos_ for token in sent]
            label = [token.label_ for token in sent.ents]

            ent_pairs , object_che = self.util.which_sent(dep, sent)
            print(ent_pairs)
            gfinal_pair = []

            pairrrr, numberrrr = self.final_ent_pairs(ent_pairs, object_che)
            gfinal_pair.append(pairrrr)

        return gfinal_pair, numberrrr


    def final_ent_pairs(self, ent_pairs, object_che):
        filtered_entpairs = [sublist for sublist in ent_pairs if not any(str(x) == '' for x in sublist)]

        # if object_che == False:
        #     pairs = pd.DataFrame(filtered_entpairs, columns=['subject', 'relation', 'subject_type'])
        # elif object_che == True:
        pairs = pd.DataFrame(filtered_entpairs, columns=['source', 'relation', 'target', 'subject_type', 'object_type'])
        # else:
        #     pass

        # print('Entity pairs extracted:', str(len(filtered_entpairs)))
        numberf = str(len(filtered_entpairs))
        # print(numberf)
        return pairs, numberf
