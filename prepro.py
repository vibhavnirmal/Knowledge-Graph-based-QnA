import spacy
import neuralcoref


class Prepro:
    """docstring for prepro."""

    def __init__(self):
        super(Prepro, self).__init__()
        self.conj_dep = {}
        self.nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(self.nlp)

    def preprocess_text(self, inputfile, coref = True):
        input_file = open(inputfile,"r+")
        text_strip = [text.strip() for text in input_file]
        preprocessed_text = [text for text in text_strip if text not in ('', ' ')]
        text = " ".join(preprocessed_text)
        text = self.nlp(text)
        text = self.nlp(text._.coref_resolved)
        return text

    def count_subj_obj(self, dep, sentence):
        count = 0
        for word in sentence.ents:
            if word.label_ in ('DATE'):
                count = count+1

        obj_cnt = dep.count('obj')+dep.count('dobj')+dep.count('pobj')
        subj_cnt = dep.count('subj')+dep.count('nsubj')+dep.count('nsubjpass')
        conj_cnt = dep.count('conj')
        time_cnt = count

        if time_cnt:
            obj_cnt = obj_cnt - time_cnt
        # print(time_cnt)
        self.conj_dep = {'obj_cnt':obj_cnt, 'subj_cnt':subj_cnt,'conj_cnt':conj_cnt,'time_cnt':time_cnt}
        return self.conj_dep

    def refine_ent(self, ent, sent):
        nlp = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(nlp)

        # print(type(ent))
        unwanted_tokens = (
            'PRON',  # pronouns
            'PART',  # particle
            'DET',  # determiner
            'SCONJ',  # subordinating conjunction
            'PUNCT',  # punctuation
            'SYM',  # symbol
            'X',  # other
            )

        if type(ent) == "<class 'spacy.tokens.token.Token'>":
            ent_type = ent.ent_type_
        else:
            ent_type = ''

        # get entity type
        if ent_type == '':
            ent_type = 'NOUN_CHUNK'
            ent = ' '.join(str(t.text) for t in
                    nlp(str(ent)) if t.pos_
                    not in unwanted_tokens and t.is_stop == False)
        elif ent_type in ('NOMINAL', 'CARDINAL', 'ORDINAL') and str(ent).find(' ') == -1:
            t = ''
            for i in range(len(sent) - ent.i):
                if ent.nbor(i).pos_ not in ('VERB', 'PUNCT'):
                    t += ' ' + str(ent.nbor(i))
                else:
                    ent = t.strip()
                    break
        # print(ent)
        return ent, ent_type
