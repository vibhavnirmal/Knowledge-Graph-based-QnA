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
        for object in sentence:
            if object.dep_ in ('obj', 'dobj', 'pobj'):
                object_che = True

                relation = [w for w in object.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    # print(relation)
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        # print(relation.nbor(1).pos_)
                        if relation.nbor(2).dep_ in ('xcomp'):
                            relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                        else:# print(relation.nbor(2).dep_)
                            relation = ' '.join((str(relation), str(relation.nbor(1))))
                            # print(relation)

                    subject = [a for a in sp_relation.lefts if a.dep_ in ('subj', 'nsubj','nsubjpass')]  # identify subject nodes
                    # print(subject)
                    if subject:
                        subject = subject[0]
                        # print(subject)
                        subject, subject_type = self.prepro.refine_ent(subject, sentence)
                        # print(subject)
                    else:
                        subject = 'unknown'
                else:
                    relation = 'unknown'

                object, object_type = self.prepro.refine_ent(object, sentence)
                self.ent_pairs = []
                # print(object, subject, relation)
                self.ent_pairs.append([str(subject).lower(), str(relation), str(object), str(subject_type), str(object_type)])
                # ent_pairs.append([str(subject).lower(), str(relation), str(object)])

                return self.ent_pairs

    def two_verbs(self, sent):
        # print(sent)
        for i in sent:
            if i.pos_ in ('PROPN'):
                subject = i

            if i.pos_ in ('VERB'):
                if i.nbor(1).pos_ in ('VERB'):
                    relation = " ".join((str(i), str(i.nbor(1))))
                else:
                    relation = str(i)

            if i.pos_ in ('NOUN'):
                print(i.nbor(1).pos_)
                if i.nbor(1).pos_ in ('ADP'):
                    if i.nbor(2).pos_ in ('NOUN'):
                        object = " ".join((str(i), str(i.nbor(1)), str(i.nbor(2))))
                    # else:
                        # object = " ".join(str(i), str(i.nbor(1)))
                else:
                    object = str(i)

            if i.pos_ in ('PRON'):
                subject = i


        # print(subject, relation, object)

        # subject, subject_type = self.prepro.refine_ent(subject, sent)
        # object, object_type = self.prepro.refine_ent(object, sent)
        self.ent_pairs = []
        self.ent_pairs.append([str(subject), str(relation), str(object), str("subject_type"), str("object_type")])
        return self.ent_pairs

    def question_pairs(self, question__):
        question__ = self.nlp(question__)

        for object in question__:
            if object.dep_ in ('obj', 'dobj', 'pobj'):
                object_che = True
                # print(object)
                relation = [w for w in object.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    # print(relation)
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        # print(relation.nbor(1).pos_)
                        if relation.nbor(2).dep_ in ('xcomp'):
                            relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                        else:# print(relation.nbor(2).dep_)
                            relation = ' '.join((str(relation), str(relation.nbor(1))))
                            # print(relation)

                    subject = [a for a in sp_relation.lefts if a.dep_ in ('subj', 'nsubj','nsubjpass')]  # identify subject nodes
                    # print(subject)
                    if subject:
                        subject = subject[0]
                        # print(subject)
                        # subject, subject_type = self.prepro.refine_ent(subject, question__)
                        # print(subject)
                    else:
                        subject = 'unknown'
                else:
                    relation = 'unknown'

                # object, object_type = self.prepro.refine_ent(object, question__)
                # print(object)
                self.ent_pairs = []
                # print(object, subject, relation)
                self.ent_pairs.append([str(subject).lower(), str(relation).lower(), str(object).lower(), str("subject_type"), str("object_type")])
                # ent_pairs.append([str(subject), str(relation), str(object)])
                # print(self.ent_pairs)
                return self.ent_pairs

    def no_object(self, sentence):
        p = [subj for subj in sentence if subj.dep_ in ('subj', 'nsubjpass', 'nsubj')]
        relation = [w for w in p[0].ancestors if w.dep_ =='ROOT']
        p[0], subject_type = self.prepro.refine_ent(p[0], sentence)
        self.ent_pairs.append([str(p[0]), str(relation[0]),str(""), str(subject_type),str("")])
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
        self.ent_pairs = []
        # print(subject_list)
        # print(object_list)
        for m in range(0, len(subject_list)):
            for n in range(0, len(object_list)):
                self.ent_pairs.append([str(pa[m][0]), str(relation), str(pb[n][0]), str("subject_type"), str("object_type")])
                # print("Hello")

        # print(self.ent_pairs)
        return self.ent_pairs
