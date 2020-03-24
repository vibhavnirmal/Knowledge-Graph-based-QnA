import spacy
import neuralcoref
from prepro import Prepro
import re

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

    def get_time_from_sent(self,sentence):
        xdate =[]
        for i in sentence.ents:
            if i.label_ in ('DATE'):
                xdate.append(str(i))
        return xdate

    def get_place_from_sent(self,sentence):
        xplace =[]
        for i in sentence.ents:
            if i.label_ in ('GPE'):
                xplace.append(str(i))
        return xplace

    def normal_sent(self, sentence):
        """ Here goes subject relation object Example:
        -> John plays cricket.
        -> Mohan solved the Tower of Hanoi problem. """
        time = self.get_time_from_sent(sentence)
        place = self.get_place_from_sent(sentence)

        subject_list, object_list = [], []
        numbers = '^[0-9]+$'

        # print(sentence)

        subject_final, aux_relation, child_with_comp = "", "", ""

        """ SUBJECT FINDING loop"""
        """
        The prime minister of INDIA
        comp comp nsubj

        Manan ate ice-cream
        nsubj ROOT comp punct obj
        """

        dep_word = [word.dep_ for word in sentence]
        word_dep_count_subj = [dep_word.index(word) for word in dep_word if word in ('nsubj', 'subj', 'nsubjpass')]
        word_dep_count_subj = word_dep_count_subj[0] + 1

        for word in sentence:
            subject_final = ""
            if word_dep_count_subj > 0:
                if word.dep_ in ('compound'):
                    if subject_final == "":
                        subject_final = str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                    else:
                        subject_final = subject_final+ " " +str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                elif word.dep_ in ('nsubj', 'subj', 'nsubjpass'):
                    subject_final = subject_final+" "+str(word)
                    subject_list.extend([str(a.text) for a in word.subtree if a.dep_ in ('conj')])
                    word_dep_count_subj = word_dep_count_subj - 1
                    break
                else:
                    pass

        subject_list.append(subject_final)
        # print(subject_list)

        for word in sentence:
            """OBJECT FINDING loop"""
            if word.dep_ in ('obj', 'dobj', 'pobj'):
                buffer_obj = word
                # print(word)

                if str(word) in place and word.nbor(-1).dep_ in ('prep') and str(word.nbor(-1)) == "of":
                    """ INDIA should be in place list + "of" "India" is there then it will come here """
                    print("came in of pobj(GPE)")
                else:
                    if str(word) not in time and str(word) not in place:
                        """ INDIA should not be in place list + INDIA should not be in time list """
                        """ice-cream and mangoes"""
                        for child in word.subtree:
                            # print(child)
                            if child.dep_ in ('conj', 'dobj', 'pobj', 'obj'):
                                if [i for i in child.lefts]:

                                    if child.nbor(-1).dep_ in ('punct') and child.nbor(-2).dep_ in ('compound'):
                                        """ice-cream"""
                                        # print("\"\"ice-cream\"\"")
                                        child = str(child.nbor(-2)) + str(child.nbor(-1)) + str(child)
                                        object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('compound'):
                                        root_word_number = [dep_word.index(word) for word in dep_word if word in ('ROOT')]
                                        obj_word_number = [dep_word.index(word) for word in dep_word if word in ('obj','pobj','dobj')]
                                        for i in reversed(range(root_word_number[0],obj_word_number[0])):
                                            if word.nbor(-i + root_word_number[0]).dep_ in ('compound'):
                                                if child_with_comp == "":
                                                    child_with_comp = str(child.nbor(-i + root_word_number[0]))
                                                else:
                                                    child_with_comp = child_with_comp +" "+ str(child.nbor(-i + root_word_number[0]))
                                        child = child_with_comp+ " " + str(child)
                                        """"ice cream"""
                                        object_list.append(str(child))
                                        # print(child, object_list, "compound")

                                    elif child.nbor(-1).dep_ in ('det'):
                                        """The Taj Mahal"""
                                        # child = str(child.nbor(-1))+ " " + str(child)
                                        # print("\"\"the ice cream\"\"")
                                        object_list.append(str(child))

                                elif [i for i in child.rights]:
                                    # print("\"\"Child Rights\"\"")
                                    if str(child.text) not in object_list:
                                        object_list.append(str(child.text))

                                    for a in child.children:
                                        if a.dep_ in ('conj'):
                                            if a.nbor(-1).dep_ in ('punct'):
                                                pass
                                            else:
                                                object_list.extend( [ str(a.text) ] )
                                            # print(a.text)
                                    # object_list.extend([str(a.text) for a in child.children if a.dep_ in ('conj')])
                                    # print(object_list)

                                else:
                                    """icecream"""
                                    # pass
                                    # print("\"\"the ice cream\"\"")
                                    if str(child) not in object_list:
                                        object_list.append(str(child))

                    elif str(word) in place and str(word.nbor(-1)) != "of":
                        object_list.append(str(word))
                    else:
                        print("no Obj")

                    # print(object_list)
                    # try:
                    #     # John Doe went college on Monday
                    #     if str(word.nbor(1).pos_) == 'ADP':
                    #         if str(word.nbor(2)) in time:
                    #             word = str(word)
                    #             # print(word, "Hello First")
                    #         else:
                    #             word = " ".join( (str(word), str(word.nbor(1)), str(word.nbor(2))) )
                    #             # print(word, "Hello Second")
                    #     elif re.match(numbers, str(word)):
                    #         print("GOT NUMBER")
                    #         pass
                    #     else:
                    #         word = word
                    #         # print(word, "elif vala part")
                    #     # else:
                    #     #     word = word
                    # except IndexError:
                    #     word = word

                    """ RELATION FINDING loop """
                    relation = [w for w in buffer_obj.ancestors if w.dep_ =='ROOT']

                    if relation:
                        relation = relation[0]
                        sp_relation = relation
                        # print(sp_relation)

                        if relation.nbor(1).pos_ in ('VERB'):
                            if relation.nbor(2).dep_ in ('xcomp'):
                                print()
                                relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                            else:
                                relation = ' '.join((str(relation), str(relation.nbor(1))))
                        elif relation.nbor(1).pos_ in ('ADP', 'PART') and relation.nbor(1).dep_ in ('aux') and str(relation.nbor(1)) == 'to':
                            # print(relation.nbor(1), relation.nbor(1).pos_ )
                            relation = " ".join((str(relation), str(relation.nbor(1))))
                            aux_relation = str(sp_relation.nbor(2))
                        else:
                            relation = str(relation)

                    else:
                        relation = 'unknown'

                    self.ent_pairs = []

                    if time:
                        time = time[0]
                    else:
                        time = " "

                    if place:
                        place = place[0]
                    else:
                        place = " "

                    pa, pb=[], []
                    for m in subject_list:
                        pa.append([m])

                    for n in object_list:
                        pb.append([n])

                    # print(subject_list, object_list)


                    for m in range(0, len(subject_list)):
                        for n in range(0, len(object_list)):
                            self.ent_pairs.append([str(pa[m][0]).lower(), str(relation).lower(),str(aux_relation).lower(), str(pb[n][0]).lower(), str(time), str(place)])

                    return self.ent_pairs

    def question_pairs(self, question__):
        # questionList = question__.split(" ")
        # print(questionList)

        questionNLPed = self.nlp(question__)
        print(questionNLPed)

        for object in questionNLPed:
            objectNEW = object
            # print(objectNEW, objectNEW.dep_)

            if object.dep_ in ('obj', 'dobj', 'pobj') and str(object).lower() != "what":
                object_che = True
                # print(object)
                # print(object.nbor(1))
                try:
                    if object.nbor(-1).pos_ in ('PUNCT') and object.nbor(-2).pos_ in ('NOUN'):
                        object = ' '.join((str(object.nbor(-2)), str(object)))
                    elif object.nbor(-1).pos_ in ('NOUN'):
                        object = ' '.join( (str(object.nbor(-1)), str(object) ))
                    # elif object.nbor(1).pos_ in ('ROOT'):
                        # pass

                except IndexError:
                    pass

                # elif object.nbor(1).pos_ in :
                    # print(object.nbor(1).pos_)

                # print(object)
                relation = [w for w in objectNEW.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    # print(relation)
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        print(relation.nbor(1).pos_)
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
                print(subject, relation, object)
                self.ent_pairs = []
                # print(object, subject, relation)
                self.ent_pairs.append([str(subject).lower(), str(relation).lower(), str(object).lower()])
                # ent_pairs.append([str(subject), str(relation), str(object)])
                # print(self.ent_pairs)
                return self.ent_pairs

            elif str(object).lower() == "what":
                object_che = True

                # print(object, "here")
                relation = [w for w in objectNEW.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    # print(sp_relation, "Jerees")
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        # print(relation.nbor(1).pos_)
                        if relation.nbor(2).dep_ in ('xcomp'):
                            relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                        else:# print(relation.nbor(2).dep_)
                            relation = ' '.join((str(relation), str(relation.nbor(1))))
                            # print(relation)

                    for jk in sp_relation.lefts:
                        if jk.dep_ in ('subj', 'nsubj','nsubjpass'):
                            for jkl in jk.lefts:
                                subject = str(jkl) + " " + str(jk)
                                print(subject)


                    # subject = [a for a in sp_relation.lefts if a.dep_ in ('subj', 'nsubj','nsubjpass')]  # identify subject nodes
                    # print(subject)
                    # if subject:
                        # subject = subject[0]
                        # print(subject)
                        # subject, subject_type = self.prepro.refine_ent(subject, question__)
                        # print(subject)
                    # else:
                        # subject = 'unknown'
                else:
                    relation = 'unknown'

                # object, object_type = self.prepro.refine_ent(object, question__)
                # print(object)
                self.ent_pairs = []
                # print(subject,relation,object)
                self.ent_pairs.append([str(subject).lower(), str(relation).lower(), str(object).lower()])
                # ent_pairs.append([str(subject), str(relation), str(object)])
                # print(self.ent_pairs)
                return self.ent_pairs

            elif object.dep_ in ('advmod'):
                # print(str(object).lower())
                if str(object).lower() == 'where':
                    relation = [w for w in object.ancestors if w.dep_ =='ROOT']
                    # print(relation)
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

                    self.ent_pairs = []
                    # print(object, subject, relation)
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(), str(object).lower()])
                    # ent_pairs.append([str(subject), str(relation), str(object)])
                    # print(self.ent_pairs)
                    return self.ent_pairs

                elif str(object).lower() == 'when':
                    relation = [w for w in object.ancestors if w.dep_ =='ROOT']
                    # print(relation)
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

                    self.ent_pairs = []
                    # print(object, subject, relation)
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(), str(object).lower(), str("when")])
                    # ent_pairs.append([str(subject), str(relation), str(object)])
                    # print(self.ent_pairs)
                    return self.ent_pairs
