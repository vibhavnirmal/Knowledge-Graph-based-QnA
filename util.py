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
        dep_count = self.prepro.count_subj_obj(dep)
        # print(dep, sent)

        conjcnt = dep_count['conj_cnt']
        subjcnt = dep_count['subj_cnt']
        objcnt = dep_count['obj_cnt']

        # for i in sent:
        #     if i.dep_ in ('obj', 'dobj', 'pobj'):
        #         if i.nbor(1).dep_ in ('nmod'):
        #             print(i)

        if ((objcnt == 1) and (subjcnt == 1)) and (conjcnt <= 0):
            # print("Sentence contains only one SUBJECT and OBJECT")
            # print(sent)
            normal_sent_ = self.complex.normal_sent(sent)
            # print(normal_sent_)
            for pair in normal_sent_:
                self.ent_pairs.append(pair)
            # print(ent_pairs)
        elif ((subjcnt == 1) and (objcnt == 0)):
            # print("Sentence contains only SUBJECT and RELATION")
            object_che = False
            no_obj_ = self.complex.no_object(sent)
            self.ent_pairs.append(no_obj_[0])
        elif ((subjcnt == 1) and (objcnt == 1) and (conjcnt >= 1)):
            # print("Sentence contains Multiple SUBJECTs and OBJECTs")
            mult_subj_obj_ = self.complex.multi_obj_subj_list(sent)
            for pair in mult_subj_obj_:
                self.ent_pairs.append(pair)
        else:
            for i in sent:
                # print(i, i.dep_)
                if i.dep_ in ('obj', 'dobj', 'pobj'):
                    try:
                        if i.nbor(1).dep_ in ('prep'):
                            if i.nbor(2).dep_ in ('pobj'):
                                multi_obj_new_pair = self.complex.two_verbs(sent)
                                for pair in multi_obj_new_pair:
                                    self.ent_pairs.append(pair)
                    except IndexError:
                        pass

        # print(subjcnt, objcnt, conjcnt)

        return self.ent_pairs, self.object_che
