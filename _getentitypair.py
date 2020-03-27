import re, spacy
import pandas as pd
from _complex import Complexx
from _resolvedep import change_nouns

class GetEntity:
    """docstring for GetEntity."""

    def __init__(self):
        super(GetEntity, self).__init__()
        self.complex = Complexx()
        self.nlp = spacy.load('en_core_web_sm')
        self.change = change_nouns()

    def preprocess_text(self, inputfile, coref = True):
        input_file = open(inputfile,"r+")
        text_strip = [text.strip() for text in input_file]
        preprocessed_text = [text for text in text_strip if text not in ('', ' ')]
        text = " ".join(preprocessed_text)
        """ ADDED CUSTOM SCRIPT """
        text = self.change.resolved(text)
        """ ___________________ """
        text = self.nlp(text)
        return text

    def get_entity(self, text):
        ent_pairs = []
        sentences = [one_sentence.string.strip() for one_sentence in text.sents]

        for one_sentence in sentences:
            final_entity_pairs = []
            one_sentence = self.nlp(one_sentence)

            dep = [token.dep_ for token in one_sentence]
            # pos = [token.pos_ for token in one_sentence]
            # label = [token.label_ for token in one_sentence.ents]

            normal_sent_ = self.complex.normal_sent(one_sentence)

            for pair in normal_sent_:
                ent_pairs.append(pair)

            pairs = pd.DataFrame(ent_pairs, columns=['source', 'relation', 'aux_relation', 'target', 'time', 'place'])
            number_of_ent_pairs = str(len(ent_pairs))

            final_entity_pairs.append(pairs)

        return final_entity_pairs, number_of_ent_pairs


if __name__ == '__main__':
    test = GetEntity()
    text = test.nlp("Vibhav ate chocolates. Vedant met Vibhav")
    entities, numbers = test.get_entity(text)
    print(entities[0])
