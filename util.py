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

        if ((objcnt == 1) and (subjcnt == 1)) and (conjcnt <= 0):
            print("SUB+OBJ")
            normal_sent_ = self.complex.normal_sent(sent)
            for pair in normal_sent_:
                self.ent_pairs.append(pair)
            # print(ent_pairs)
        elif ((subjcnt == 1) and (objcnt == 0)):
            print("SUBJ")
            object_che = False
            no_obj_ = self.complex.no_object(sent)
            self.ent_pairs.append(no_obj_[0])
        elif ((subjcnt == 1) and (objcnt == 1) and (conjcnt >= 1)):
            print("SUBJ+OBJ+Multi")
            mult_subj_obj_ = self.complex.multi_obj_subj_list(sent)
            for pair in mult_subj_obj_:
                self.ent_pairs.append(pair)
        else:
            pass

        print(subjcnt, objcnt, conjcnt)

        return self.ent_pairs, self.object_che
