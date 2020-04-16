import spacy, re

class ComplexFunc:
    """docstring for Tenses."""

    def __init__(self):
        self.ent_pairs = list()
        self.nlp = spacy.load('en_core_web_sm')

    def get_time_place_from_sent(self,sentence):
        xdate =[]
        xplace =[]
        for i in sentence.ents:
            if i.label_ in ('DATE'):
                xdate.append(str(i))

            if i.label_ in ('GPE'):
                xplace.append(str(i))

        return xdate, xplace

    def find_obj(self, sentence, place, time):
        object_list = []

        for word in sentence:
            """OBJECT FINDING loop"""
            if word.dep_ in ('obj', 'dobj', 'pobj'):
                buffer_obj = word

                if str(word) in place and word.nbor(-1).dep_ in ('prep') and str(word.nbor(-1)) == "of":
                    """ INDIA should be in place list + "of" "India" is there then it will come here """
                else:
                    if str(word) not in time and str(word) not in place:
                        """ INDIA should not be in place list + INDIA should not be in time list """
                        """ice-cream and mangoes"""
                        for child in word.subtree:
                            if child.dep_ in ('conj', 'dobj', 'pobj', 'obj') and (str(child) not in time) and (str(child) not in place):
                                if [i for i in child.lefts]:
                                    if child.nbor(-1).dep_ in ('nummod') and child.dep_ in ('dobj', 'obj','pobj'):
                                        child = str(child.nbor(-1)) + " " + str(child)
                                        object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('punct'):
                                        if child.nbor(-2).dep_ in ('compound'):
                                            """ice-cream"""
                                            child = str(child.nbor(-2)) + str(child.nbor(-1)) + str(child)
                                            object_list.append(str(child))
                                        elif child.nbor(-2).dep_ in ('amod'):
                                            """ social-distancing """
                                            child = str(child.nbor(-2)) + str(child.nbor(-1)) + str(child)
                                            object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('compound'):
                                        # print(child)
                                        child_with_comp = ""
                                        for i in child.subtree:
                                            if i.dep_ in ('compound', 'nummod','quantmod'):
                                                if child_with_comp == "":
                                                    child_with_comp = str(i)
                                                else:
                                                    child_with_comp = child_with_comp +" "+ str(i)
                                            elif i.dep_ in ('cc'):
                                                break
                                        child = child_with_comp + " " + str(child)
                                        """"ice cream"""
                                        object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('det'):
                                        """The Taj Mahal"""
                                        object_list.append(str(child))

                                elif [i for i in child.rights]:
                                    if str(child.text) not in object_list:
                                        object_list.append(str(child.text))

                                    for a in child.children:
                                        if a.dep_ in ('conj'):
                                            if a.nbor(-1).dep_ in ('punct'):
                                                pass
                                            else:
                                                object_list.extend( [ str(a.text) ] )

                                else:
                                    """icecream"""
                                    if str(child) not in object_list:
                                        object_list.append(str(child))

                    elif str(word) in place and str(word.nbor(-1)) != "of":
                        if object_list == []:
                            object_list.append(str(word))
                        else:
                            pass
                    else:
                        if str(word) in time and object_list == []:
                            object_list.append(str(word))

        return object_list, buffer_obj

    def find_subj(self, sentence):
        subject_list = []
        """ SUBJECT FINDING loop"""
        dep_word = [word.dep_ for word in sentence]
        word_dep_count_subj = [dep_word.index(word) for word in dep_word if word in ('nsubj', 'subj', 'nsubjpass')]
        if word_dep_count_subj:
            word_dep_count_subj = word_dep_count_subj[0] + 1
        else:
            word_dep_count_subj = 1

        subject_final = ""
        for word in sentence:
            # print(word.dep_, word)
            if word_dep_count_subj > 0:
                """ IN prime minister it gives compound and then nmod """
                if word.dep_ in ('compound') or word.dep_ in ('nmod') or word.dep_ in ('amod') or word.dep_ in ('poss') or word.dep_ in ('case') or word.dep_ in ('nummod'):
                    if subject_final == "":
                        subject_final = str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                    elif word.dep_ in ('case'):
                        subject_final = subject_final+ "" +str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                    else:
                        subject_final = subject_final+ " " +str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                elif word.dep_ in ('nsubj', 'subj', 'nsubjpass'):
                    if subject_final == "":
                        subject_final = str(word)
                        subject_list.extend([str(a.text) for a in word.subtree if a.dep_ in ('conj')])
                        word_dep_count_subj = word_dep_count_subj - 1
                        break
                    else:
                        subject_final = subject_final+" "+str(word)
                        subject_list.extend([str(a.text) for a in word.subtree if a.dep_ in ('conj')])
                        word_dep_count_subj = word_dep_count_subj - 1
                        break
                else:
                    pass

        subject_list.append(subject_final)
        return subject_list

    def find_relation(self, buffer_obj):
        aux_relation = ""
        """ RELATION FINDING loop """
        relation = [w for w in buffer_obj.ancestors if w.dep_ =='ROOT']

        if relation:
            relation = relation[0]
            sp_relation = relation
            if relation.nbor(1).pos_ in ('VERB'):
                if relation.nbor(2).dep_ in ('xcomp'):
                    relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                else:
                    relation = str(relation)
                    if str(sp_relation.nbor(2)) != 'and':
                        if sp_relation.nbor(1).dep_ in ('xcomp'):
                            aux_relation = str(sp_relation.nbor(1))
                        else:
                            aux_relation = str(sp_relation.nbor(2))
            elif relation.nbor(1).pos_ in ('ADP', 'PART') and relation.nbor(1).dep_ in ('aux') and str(relation.nbor(1)) == 'to':
                # print(relation.nbor(1), relation.nbor(1).pos_ )
                # print(relation)
                relation = " ".join((str(relation), str(relation.nbor(1))))
                if str(sp_relation.nbor(2)) != 'and':
                    aux_relation = str(sp_relation.nbor(2))
            elif relation.nbor(1).dep_ in ('prep') and str(relation.nbor(1)) == 'to' and (relation.nbor(1)).dep_ not in ('obj','dobj','pobj','det'):
                # print(relation.nbor(1), relation.nbor(1).pos_ )
                # print(relation)
                relation = " ".join((str(relation), str(relation.nbor(1))))
            else:
                relation = str(relation)
        else:
            relation = 'unknown'

        return relation, aux_relation

    def normal_sent(self, sentence):
        time, place = self.get_time_place_from_sent(sentence)

        subject_list, object_list = [], []

        aux_relation, child_with_comp = "", ""

        subject_list = self.find_subj(sentence)
        object_list, buffer_obj = self.find_obj(sentence, place, time)
        relation, aux_relation = self.find_relation(buffer_obj)

        self.ent_pairs = []

        if time:
            time = time[0]
        else:
            time = ""

        if place:
            place = place[0]
        else:
            place = ""

        pa, pb=[], []
        for m in subject_list:
            pa.append([m])

        for n in object_list:
            pb.append([n])

        # print(pa, pb)

        for m in range(0, len(pa)):
            for n in range(0, len(pb)):
                self.ent_pairs.append([str(pa[m][0]).lower(), str(relation).lower(),str(aux_relation).lower(), str(pb[n][0]).lower(), str(time), str(place)])

        # print(self.ent_pairs)
        return self.ent_pairs

    def question_pairs(self, question__):
        # questionList = question__.split(" ")
        # print(questionList)

        questionNLPed = self.nlp(question__)
        maybe_object = ([i for i in questionNLPed if i.dep_ in ('obj', 'pobj', 'dobj')])
        # print(maybe_object)
        maybe_place, maybe_time = [], []
        aux_relation = ""
        maybe_time, maybe_place = self.get_time_place_from_sent(questionNLPed)
        # print()
        object_list = []


        for object in questionNLPed:
            objectNEW = object
            # print(object.dep_)

            """ FOR WHO """
            if object.dep_ in ('obj', 'dobj', 'pobj', 'xcomp') and str(object).lower() != "what":
                buffer_obj = object

                if object.dep_ in ('xcomp') and object.nbor(-1).dep_ in ('aux') and object.nbor(-2).dep_ in ('ROOT'):
                    # print("here")
                    continue

                if str(object) in maybe_place and object.nbor(-1).dep_ in ('prep') and str(object.nbor(-1)) == "of":
                    """ INDIA should be in place list + "of" "India" is there then it will come here """
                else:
                    if str(object) not in maybe_time and str(object) not in maybe_place:
                        """ INDIA should not be in place list + INDIA should not be in time list """
                        """ice-cream and mangoes"""
                        for child in object.subtree:
                            # print(child)
                            if child.dep_ in ('conj', 'dobj', 'pobj', 'obj'):
                                if [i for i in child.lefts]:
                                    if child.nbor(-1).dep_ in ('punct') and child.nbor(-2).dep_ in ('compound'):
                                        """ice-cream"""
                                        child = str(child.nbor(-2)) + str(child.nbor(-1)) + str(child)
                                        object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('compound'):
                                        # print(child)
                                        child_with_comp = ""
                                        for i in child.subtree:
                                            if i.dep_ in ('compound', 'nummod','quantmod'):
                                                if child_with_comp == "":
                                                    child_with_comp = str(i)
                                                else:
                                                    child_with_comp = child_with_comp +" "+ str(i)
                                            elif i.dep_ in ('cc'):
                                                break
                                        child = child_with_comp + " " + str(child)

                                        """"ice cream"""
                                        # print(child)
                                        object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('det'):
                                        """The Taj Mahal"""
                                        object_list.append(str(child))

                                elif [i for i in child.rights]:
                                    if str(child.text) not in object_list:
                                        object_list.append(str(child.text))

                                    for a in child.children:
                                        if a.dep_ in ('conj'):
                                            if a.nbor(-1).dep_ in ('punct'):
                                                pass
                                            else:
                                                object_list.extend( [ str(a.text) ] )

                                else:
                                    """icecream"""
                                    if str(child) not in object_list:
                                        object_list.append(str(child))

                            elif object.dep_ in ('xcomp'):
                                object_list.append(str(object))

                    elif str(object) in maybe_place and str(object.nbor(-1)) != "of":
                        object_list.append(str(object))
                    else:
                        if str(object) in time and object_list == []:
                            object_list.append(str(object))


                # print(object_list)
                object = object_list[-1]
                # # print(object)
                # # print(object.nbor(1))
                # try:
                #     if object.nbor(-1).pos_ in ('PUNCT') and object.nbor(-2).pos_ in ('NOUN'):
                #         object = ' '.join((str(object.nbor(-2)), str(object)))
                #     elif object.nbor(-1).pos_ in ('NOUN'):
                #         object = ' '.join( (str(object.nbor(-1)), str(object) ))
                #     # elif object.nbor(1).pos_ in ('ROOT'):
                #         # pass
                # except IndexError:
                #     pass

                # elif object.nbor(1).pos_ in :
                    # print(object.nbor(1).pos_)

                # print(object)
                relation = [w for w in objectNEW.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    # print(sp_relation)
                    # print(relation)
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        if relation.nbor(2).dep_ in ('xcomp'):
                            aux_relation = str(relation.nbor(2))
                            relation = str(relation)+" "+str(relation.nbor(1))
                        else:# print(relation.nbor(2).dep_)
                            relation = str(relation)
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
                # print(subject, relation, object)
                self.ent_pairs = []

                if maybe_time and maybe_place:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str(maybe_time[0]).lower(), str(maybe_place[0]).lower()])
                elif maybe_time:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str(maybe_time[0]).lower(), str("").lower()])
                elif maybe_place:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str("").lower(), str(maybe_place[0]).lower()])
                else:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str("").lower(), str("").lower()])
                # ent_pairs.append([str(subject), str(relation), str(object)])
                # print(self.ent_pairs)
                return self.ent_pairs

            elif str(object).lower() == "what":
                relation = [w for w in objectNEW.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        if relation.nbor(2).dep_ in ('xcomp'):
                            aux_relation = str(relation.nbor(2))
                            relation = str(relation)+" "+str(relation.nbor(1))
                        else:# print(relation.nbor(2).dep_)
                            relation = str(relation)
                            # print(relation)

                    subject = self.find_subj(questionNLPed)
                    # print(subject)
                    subject = subject[-1]

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
                if maybe_time and maybe_place:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str(maybe_time[0]).lower(), str(maybe_place[0]).lower()])
                elif maybe_time:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str(maybe_time[0]).lower(), str("").lower()])
                elif maybe_place:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str("").lower(), str(maybe_place[0]).lower()])
                else:
                    self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(object).lower(), str("").lower(), str("").lower()])
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
                            if relation.nbor(2).dep_ in ('xcomp'):
                                aux_relation = str(relation.nbor(2))
                                relation = str(relation)+" "+str(relation.nbor(1))
                            else:# print(relation.nbor(2).dep_)
                                relation = str(relation)
                                # print(relation)

                        # for left_word in sp_relation.lefts:
                        #     if left_word.dep_ in ('subj', 'nsubj','nsubjpass'):
                        #         if [i for i in left_word.lefts]:
                        #             for left_of_left_word in left_word.lefts:
                        #                 subject = str(left_of_left_word) + " " + str(left_word)
                        #         else:
                        #             subject = str(left_word)

                        subject = self.find_subj(questionNLPed)
                        # print(subject)
                        subject = subject[-1]

                        # subject = [a for a in sp_relation.lefts if a.dep_ in ('subj', 'nsubj','nsubjpass')]  # identify subject nodes
                        # # print(subject)
                        # if subject:
                        #     subject = subject[0]
                        #     # print(subject)
                        #     # subject, subject_type = self.prepro.refine_ent(subject, question__)
                        #     # print(subject)
                        # else:
                        #     subject = 'unknown'
                    else:
                        relation = 'unknown'

                    self.ent_pairs = []
                    # print(object, subject, relation)
                    if maybe_object:
                        if maybe_time and maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_time:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("").lower(), str("where").lower()])
                        else:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("").lower(), str("where").lower()])
                    else:
                        if maybe_time and maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_time:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("").lower(), str("where").lower()])
                        else:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("").lower(), str("where").lower()])

                    # ent_pairs.append([str(subject), str(relation), str(object)])
                    # print(self.ent_pairs)

                    return self.ent_pairs

                elif str(object).lower() == 'when':
                    # print(object)
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

                        for left_word in sp_relation.lefts:
                            if left_word.dep_ in ('subj', 'nsubj','nsubjpass'):
                                if [i for i in left_word.lefts]:
                                    for left_of_left_word in left_word.lefts:
                                        subject = str(left_of_left_word) + " " + str(left_word)
                                else:
                                    subject = str(left_word)
                        # subject = [a for a in sp_relation.lefts if a.dep_ in ('subj', 'nsubj','nsubjpass')]  # identify subject nodes
                        # # print(subject)
                        # if subject:
                        #     subject = subject[0]
                        #     # print(subject)
                        #     # subject, subject_type = self.prepro.refine_ent(subject, question__)
                        #     # print(subject)
                        # else:
                        #     subject = 'unknown'
                    else:
                        relation = 'unknown'

                    self.ent_pairs = []
                    # print(object, subject, relation)
                    if maybe_object:
                        if maybe_time and maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        elif maybe_time:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str("").lower()])
                        elif maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        else:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str("").lower()])
                    else:
                        if maybe_time and maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        elif maybe_time:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str("").lower()])
                        elif maybe_place:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        else:
                            self.ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str("").lower()])

                    # ent_pairs.append([str(subject), str(relation), str(object)])
                    # print(self.ent_pairs)
                    return self.ent_pairs
