import spacy
from complex import Complexx
from prepro import Prepro

class Utility:
    """docstring for utility."""

    def __init__(self):
        super(Utility, self).__init__()
        self.ent_pairs = []
        self.complex = Complexx()
        self.prepro = Prepro()
        self.object_che = True

    def which_sent(self, dep, sent):
        dep_count = self.prepro.count_subj_obj(dep, sent)

        conjcnt = dep_count['conj_cnt']
        subjcnt = dep_count['subj_cnt']
        objcnt = dep_count['obj_cnt']
        timecnt = dep_count['time_cnt']
        # print(conjcnt, subjcnt, objcnt)

        root_word = [word for word in sent if word.dep_ in ('ROOT')]

        normal_sent_ = self.complex.normal_sent(sent)
        for pair in normal_sent_:
            self.ent_pairs.append(pair)

        # if root_word:
        #     if root_word[0].nbor(1).dep_ in ('prep', 'aux') and root_word[0].nbor(2).dep_ in ('xcomp', 'advcl'):
        #         """Check For: verb + to + verb """
        #         multi_obj_new_pair = self.complex.two_verbs(sent)
        #         for pair in multi_obj_new_pair:
        #             self.ent_pairs.append(pair)
        # elif ((subjcnt == 1) and (objcnt == 1)) and (conjcnt <= 0):
        #     print("Sentence contains only one SUBJECT and OBJECT")
        #     normal_sent_ = self.complex.normal_sent(sent)
        #     for pair in normal_sent_:
        #         self.ent_pairs.append(pair)
        # elif ((subjcnt >= 1) and (objcnt >= 1) and (conjcnt >= 1)):
        #     print("Sentence contains Multiple SUBJECTs and OBJECTs")
        #     mult_subj_obj_ = self.complex.multi_obj_subj_list(sent)
        #     for pair in mult_subj_obj_:
        #         self.ent_pairs.append(pair)
        # else:
        #     pass

        return self.ent_pairs
