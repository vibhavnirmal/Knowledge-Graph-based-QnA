import spacy
import neuralcoref
from prepro import Prepro

class Complexx:
    """docstring for Tenses."""

    def __init__(self):
        self.self = self
        self.x = 0
        self.ent_pairs = list()
        self.prepro = Prepro()
        self.count = 0
        self.nlp = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(self.nlp)

    def multi_child(self, token):
        tok_childs = [child for child in token.children if child.dep_ in ('conj')]
        return tok_childs

    def normal_sent(self, sentence):
        """ Here goes subject relation object Example: Someone plays cricket. """
        self.ent_pairs = []
        # print(sentence, "HEREEE")

        for token in sentence:
            if token.dep_ in ('ROOT'):
                relation = token
                subject = [i for i in relation.lefts if i.dep_ in ('subj', 'nsubjpass', 'nsubj')]
                # print(subject)
                object = [i for i in relation.rights if i.dep_ in ('obj', 'dobj', 'pobj')]
                # print(object)
                # print(subject[0], relation, object[0])

        if subject and object:
            subject, subject_type = self.prepro.refine_ent(subject, sentence)
            object, object_type = self.prepro.refine_ent(object, sentence)
            # print(subject_type, "OLOOOOO")

        self.ent_pairs.append([str(subject), str(relation), str(object), str(subject_type), str(object_type)])
        # print(self.ent_pairs, "HOLAAAA")
        return self.ent_pairs

    def no_object(self, sentence):
        p = [subj for subj in sentence if subj.dep_ in ('subj', 'nsubjpass', 'nsubj')]
        relation = [w for w in p[0].ancestors if w.dep_ =='ROOT']
        p[0], subject_type = self.prepro.refine_ent(p[0], sentence)
        self.ent_pairs.append([str(p[0]), str(relation[0]), str(subject_type)])
        return self.ent_pairs

    def multi_obj_subj_list(self, sentence):
        subject_list, object_list = [], []
        for i in sentence:
            if i.dep_ in ('subj', 'nsubj', 'nsubjpass'):
                subject_list.append(i)
                subject_list.extend([a.text for a in i.subtree if a.dep_ in ('conj')])
            elif i.dep_ in ('obj', 'pobj', 'dobj'):
                object_list.append(i)
                object_list.extend([b.text for b in i.subtree if b.dep_ in ('conj')])
            elif i.dep_ in ('ROOT'):
                relation = i
            else:
                pass

        # print(subject_list, object_list)
        pa, pb=[], []
        for m in subject_list:
            m, subject_type = self.prepro.refine_ent(m, sentence)
            pa.append([m, subject_type])
        # print(pa)

        for n in object_list:
            n, object_type = self.prepro.refine_ent(n, sentence)
            pb.append([n, object_type])
        # print(pb)

        # print(object, subject, relation)
        # print(subject_list)
        # print(object_list)
        for m in range(0, len(subject_list)):
            for n in range(0, len(object_list)):
                self.ent_pairs.append([str(pa[m][0]), str(relation), str(pb[n][0]), str(pa[n][1]), str(pb[n][1])])
                # print("Hello")

        # print(self.ent_pairs)
        return self.ent_pairs
