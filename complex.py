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
        print(sentence)
        for token in sentence:
            if token.dep_ in ('ROOT'):
                relation = token
                subject = [i for i in relation.lefts if i.dep_ in ('subj', 'nsubjpass', 'nsubj')]
                object = [i for i in relation.rights if i.dep_ in ('obj', 'dobj', 'pobj')]
                # print(subject[0], relation, object[0])

        subject, subject_type = self.prepro.refine_ent(subject, sentence)
        object, object_type = self.prepro.refine_ent(object, sentence)
        self.ent_pairs.append([str(subject), str(relation), str(object), str(subject_type), str(object_type)])
        return self.ent_pairs

    def no_object(self, sentence):
        p = [subj for subj in sentence if subj.dep_ in ('subj', 'nsubjpass', 'nsubj')]
        relation = [w for w in p[0].ancestors if w.dep_ =='ROOT']
        p[0], subject_type = self.prepro.refine_ent(p[0], sentence)
        self.ent_pairs.append([str(p[0]), str(relation[0]), str(subject_type)])
        return self.ent_pairs

    def two_diff_sent(self, sentence):
        # print(sentence)
        x = []
        count = 0
        for word in sentence:
            count += 1
            if word.dep_ in ('cc'):
                p1 = count-1
                x.append(p1)
        print(x)

        depen = []
        for i in x:
            depen.append([word.dep_ for word in sentence[:i]])

        print(depen)
        newcount = -1
        senten1, senten2 = "", ""
        # , ["subj", "ROOT", "dobj"], ["subj", "ROOT", "pobj"], ["nsubj", "ROOT", "obj"], ["nsubj", "ROOT", "dobj"], ["nsubj", "ROOT", "pobj"], ["nsubjpass", "ROOT", "obj"], ["nsubjpass", "ROOT", "dobj"], ["nsubjpass", "ROOT", "pobj"]]

        list2 = ["nsubj", "ROOT", "dobj"]
        for i in depen:
            newcount += 1
            list1 = i
            check = all(item in list1 for item in list2)
            print(check)
            if check:
                lista = [str(w) for w in sentence]

                p1 = lista[:x[newcount]]
                p2 = lista[x[newcount]+1:]

                senten1 = " ".join(p1)
                senten2 = " ".join(p2)

                senten1 = self.nlp(senten1)
                senten2 = self.nlp(senten2)

        print(senten1)
        print(senten2)

        return senten1, senten2
            # self.normal_sent(self.nlp(senten2))


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
            pb.append([n, subject_type])
        # print(pb)

        # print(object, subject, relation)
        for m in range(0, len(subject_list)):
            for n in range(0, len(object_list)):
                self.ent_pairs.append([str(pa[m][0]), str(relation), str(pb[n][0]), str(subject_type), str(object_type)])

        return self.ent_pairs
