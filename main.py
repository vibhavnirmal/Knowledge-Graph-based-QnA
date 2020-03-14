import re
import spacy
import neuralcoref
import pandas as pd
from complex import Complexx
from prepro import Prepro
from util import Utility


class mainFunc:
    """docstring for main."""

    def __init__(self):
        super(mainFunc, self).__init__()
        self.complex = Complexx()
        self.prepro = Prepro()
        self.util = Utility()
        self.sentence_of_mine = ""
        self.nlp = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(self.nlp)

    def get_entity(self, filename, coref = True):
        with open(filename,"r+") as new:
            for text in new:
                # print(text)
                text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
                text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
                text = self.nlp(text)

            if coref:
                text = self.nlp(text._.coref_resolved)  # resolve coreference clusters

        sentences = [sent.string.strip() for sent in text.sents]  # split text into sentences
        # print(sentences)

        for sent in sentences:
            sent = self.nlp(sent)

            # self.sentence_of_mine = sent
            #
            # spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
            # spans = spacy.util.filter_spans(spans)
            # # print(spans)
            # with sent.retokenize() as retokenizer:
            #     [retokenizer.merge(span) for span in spans]
            #
            # dep = [token.dep_ for token in sent]
            # print(dep)

            # ent_pairs , object_che = self.util.which_sent(dep, sent)
            # print(ent_pairs)

            sent1, sent2 = self.complex.two_diff_sent(sent)

            text = str(sent1) + ". " +str(sent2)
            text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
            text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
            text = self.nlp(text)
            text = self.nlp(text._.coref_resolved)
            # print(text)

        sentencesgg = [sent.string.strip() for sent in text.sents]
        # print(sentences)

        for sent in sentencesgg:
            sent = self.nlp(sent)

            spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
            spans = spacy.util.filter_spans(spans)
            # print(spans)
            with sent.retokenize() as retokenizer:
                [retokenizer.merge(span) for span in spans]

            dep = [token.dep_ for token in sent]
            # print(dep)

            ent_pairs , object_che = self.util.which_sent(dep, sent)
            # print(ent_pairs)

        filtered_entpairs = [sublist for sublist in ent_pairs if not any(str(x) == '' for x in sublist)]

        if object_che == False:
            pairs = pd.DataFrame(filtered_entpairs, columns=['subject', 'relation', 'subject_type'])
        elif object_che == True:
            pairs = pd.DataFrame(filtered_entpairs, columns=['subject', 'relation', 'object', 'subject_type', 'object_type'])
        else:
            pass

        print('Entity pairs extracted:', str(len(filtered_entpairs)))
        print(pairs)
