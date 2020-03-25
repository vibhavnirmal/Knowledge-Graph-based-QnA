import spacy

class change_nouns:
    """docstring for change_nouns."""

    def __init__(self):
        super(change_nouns, self).__init__()
        self.nlp = spacy.load('en_core_web_sm')

    def resolved(self, text):
        text = self.nlp(text)
        flag = True

        sentences = []

        for sent in text.sents:
            for word in sent:
                if word.dep_ in ('nsubj','subj','nsubjpass'):
                    if str(word) in ('he','HE', 'He','she','SHE', 'She','it','IT', 'It'):
                        new_word = last_word
                        sentences.append(str(sent).replace(str(word), str(new_word)))
                        flag = False

                if word.dep_ in ('nsubj','subj','nsubjpass') and str(word) not in ('he','HE', 'He','she','SHE', 'She','it','IT', 'It'):
                    last_word = word

            if flag:
                sentences.append(str(sent))
            else:
                flag = True

        resolved_text = " ".join(sentences)
        return resolved_text


if __name__ == "__main__":
    k = change_nouns()
    sentences = k.resolved("Vibhav plays cricket. He ate ice-cream.")
    print(sentences)
